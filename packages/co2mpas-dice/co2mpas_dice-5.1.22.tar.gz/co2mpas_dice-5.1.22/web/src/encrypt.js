(function () {
    "use strict";
    const Tar = require("tar-js/lib/tar");
    const pako = require("pako");
    const forge = require('node-forge/lib/index');
    const XLSX = require("xlsx")
    const JSZip = require("jszip");
    const jsyaml = require("js-yaml");
    const Ajv = require('ajv');
    const deref = require("json-schema-deref-sync");
    const cov = require('compute-covariance');
    const JET_version = require('../package.json').version

    function make_hash() {
        let md = forge.md.sha256.create();
        Array.from(arguments).forEach(v => md.update(v));
        return forge.util.bytesToHex(md.digest().getBytes())
    }

    const getRandom99 = () => (Math.floor(forge.util.createBuffer(forge.random.getBytesSync(1)).getInt(8) / 2.56));
    const aes_encrypt = (plaintext, associated_data) => {
        var key = forge.random.getBytesSync(32);
        var iv = forge.random.getBytesSync(16);
        var cipher = forge.cipher.createCipher('AES-GCM', key);
        cipher.start({
            iv: iv,
            additionalData: associated_data
        });
        cipher.update(forge.util.createBuffer(plaintext, 'binary'));
        cipher.finish();
        return {
            key: {
                key: key,
                iv: iv,
                tag: cipher.mode.tag.getBytes()
            },
            data: cipher.output.getBytes()
        }
    };
    const rsa_encrypt = (rsaKey, plaintext) => {
        return rsaKey.encrypt(
            plaintext, 'RSA-OAEP', {
                md: forge.md.sha256.create(),
                mgf1: {
                    md: forge.md.sha256.create()
                }
            }
        )
    }
    const encrypt_data = (data2encrypt, secretKey, serverKey, associated_data) => {
        let {
            key,
            data
        } = aes_encrypt(pako.deflate(jsyaml.safeDump(data2encrypt, {condenseFlow: true})), associated_data);
        key = rsa_encrypt(secretKey, (
            'iv: !!binary |\n  ' + forge.util.encode64(key.iv) +
            '\nkey: !!binary |\n  ' + forge.util.encode64(key.key) +
            '\ntag: !!binary |\n  ' + forge.util.encode64(key.tag) + '\n'
        ));
        let md = forge.md.sha256.create();
        md.update(key);
        md.update(data);
        let verify = forge.util.encode64(rsa_encrypt(serverKey, md.digest().getBytes()));
        return {
            verify,
            encrypted: {
                key: forge.util.encode64(key),
                data: forge.util.encode64(data)
            }
        }
    }
    const sign_data = (privateKey, data) => {
        var md = forge.md.sha256.create();
        md.update(data);
        var pss = forge.pss.create({
            md: forge.md.sha256.create(),
            mgf: forge.mgf.mgf1.create(forge.md.sha256.create()),
            saltLength: ((2048 - 1 - 256) / 8).toFixed(0) - 2
        });
        return forge.util.bytesToHex(privateKey.sign(md, pss));
    }
    const matchParamName = text => {
        let found = /^\s*((plan|base|flag|dice)|(target|input|output|data|meta)|((calibration|prediction)s?)|((WLTP|NEDC|ALL)([-_][HLM])?))\s*$/gmi.exec(text);
        if (found)
            return {param: found[1]}
        found = /^(flag)[.\s]+(input_version|vehicle_family_id)\s*([.\s]+ALL)?$/gmi.exec(text);
        if (found)
            return {scope: found[1], flag: found[2]}
        found = /^(dice)[.\s]+(.+)([.\s]+ALL)\s*$/gmi.exec(text);
        if (found)
            return {scope: found[1].replace(/[.\s]+$/g, ''), dice: found[2]}
        found = /^(dice)[.\s]+(.+)$/gmi.exec(text);
        if (found)
            return {scope: found[1].replace(/[.\s]+$/g, ''), dice: found[2]}
        found = /^(meta)[.\s]+((.+)[.\s]+)?([^.\s]+)\s*$/gmi.exec(text);
        if (found) {
            if (/^(WLTP|NEDC|ALL)([-_][HLM])?$/gmi.exec(found[4])) {
                text = found[1] + '.' + (found[4].toUpperCase() !== 'ALL' ? found[4] : '') + '.' + found[3];
                found = /^(meta)[.\s]+((.+)[.\s]+)?([^.\s]+)[.\s]*$/gmi.exec(text)
            }
            return {scope: found[1], meta: found[3], param: found[4]}
        }
        found = /^((base)[.\s]+)?((target|input|output|data)s?[.\s]+)?((calibration|prediction)s?[.\s]+)?(((WLTP|NEDC|ALL)([-_][HLM])?)[.\s]+)?([^.\s]*)\s*$/gmi.exec(text);
        if (found && found[0].replace(/[\n\s]*/g, ''))
            return {
                scope: found[2],
                usage: found[4],
                stage: found[6],
                cycle: found[8],
                param: found[11]
            }
        found = /^((base)[.\s]+)?((target|input|output|data)s?[.\s]+)?((calibration|prediction)s?[.\s]+)?([^.\s]*)([.\s]+((WLTP|NEDC|ALL)([-_][HLM])?))?\s*$/gmi.exec(text);
        if (found && found[0].replace(/[\n\s]*/g, ''))
            return {
                scope: found[2],
                usage: found[4],
                stage: found[6],
                cycle: found[9],
                param: found[7]
            }
    }
    const matchSheetName = text => {
        let found = /^(flag|dice)([.\s]+(pa|ts|mt))?\s*$/gmi.exec(text);
        if (found)
            return {scope: found[1], type: found[3]}
        found = /^(meta)([.\s]+(.+))?[.\s]+(pa|ts|mt)[.\s]*$/gmi.exec(text);
        if (found)
            return {scope: found[1], meta: found[3], type: found[4]}
        found = /^((base)[.\s]*)?((target|input|output|data)s?[.\s]*)?((calibration|prediction)s?[.\s]*)?(((WLTP|NEDC|ALL)([-_][HLM])?)[.\s]*)?((pa|ts|mt)[.\s]*)?$/gmi.exec(text);
        if (found && found[0].replace(/[\n.\s]*/g, ''))
            return {
                scope: found[2],
                usage: found[4],
                stage: found[6],
                cycle: found[8],
                type: found[12]
            }
    }
    const getSheetType = match => {
        if (match.type)
            return match.type;
        return (["flag", "dice"].includes(match.scope) || (!match.cycle)) ? "pa" : "ts"
    }
    const getCycle = match => {
        if (!match.cycle)
            return ['wltp_h', 'wltp_l', 'wltp_m'];
        if (match.cycle === "all")
            return ['wltp_h', 'wltp_l', 'wltp_m'];
        if (match.cycle === "wltp")
            return ['wltp_h', 'wltp_l', 'wltp_m'];
        if (match.cycle === "nedc")
            return ['nedc_h', 'nedc_l'];
        if (['all-h', 'all_h'].includes(match.cycle))
            return ['wltp_h'];
        if (['all-l', 'all_l'].includes(match.cycle))
            return ['wltp_l'];
        if (['all-m', 'all_m'].includes(match.cycle))
            return ['wltp_m'];
        if ((typeof match.cycle) === "string")
            return [match.cycle.replace("-", "_")];
    }
    const getStage = match => {
        if (match.stage) {
            return match.stage.replace(/\s/g, '')
        } else {
            return (/nedc/g.exec(match.cycle || '') || match.usage === 'target') ? 'prediction' : 'calibration'
        }
    }
    const parseKey = match => {
        if (match.scope === 'flag')
            return [[match.flag === 'vehicle_family_id' ? 'dice' : match.scope, match.flag]]
        if (match.scope === 'dice')
            return [[match.scope, match.dice]]
        if (match.scope === 'meta')
            return [[match.scope, (match.meta || '').replace(/(\s*\.\s*|\s+)/g, '.').replace(/-/g, '_'), match.param]]
        if (match.scope === 'base') {
            let param = match.param.toLowerCase()
            if (param.toLowerCase() === 'version')
                return [['flag', 'input_version']]
            return getCycle(match).map(cycle => ([match.scope, match.usage, getStage(Object.assign({}, match, {cycle: cycle})), cycle, param]))
        }
    }
    const isEmpty = value => {
        if (value === null || value === undefined)
            return true
        if ((typeof value) === 'number')
            return (!value && value !== 0) || Number.isNaN(value)
        if ((typeof value) === 'object')
            return value.length < 1 || (Array.isArray(value) && !value.some(v => !isEmpty(v)))
        return false
    }
    const dropNulls = array => array.filter(r => (!r.every(v => (v === undefined || v === null))))
    const filterMatch = match => {
        if (match) {
            let m = {};
            Object.keys(match).forEach(i => {
                let j = match[i]
                if (j)
                    m[i] = j.toLowerCase()
            })
            return m
        }
    }
    const parseValues = (data, dfl, where, values, errors) => {
        dfl = dfl || {};
        let keys = [];
        Object.keys(data).forEach(k => {
            let value = data[k];
            k = k.trim()
            let match = matchParamName(k)
            if (!match && dfl.scope === 'meta')
                match = matchParamName(['meta', dfl.meta, k].filter(v => v).join('.'))
            if (!match) {
                errors.push({
                    type: 'debug',
                    msg: "Parameter '" + k + "' " + where + " cannot be parsed!"
                })
            } else if (!isEmpty(value)) {
                parseKey(Object.assign({}, dfl, filterMatch(match))).forEach(key => {
                    keys.push(key)
                    let r = values, n = key.length - 1;
                    key.slice(0, n).forEach(k => {
                        if (!r.hasOwnProperty(k))
                            r[k] = {}
                        r = r[k]
                    })
                    r[key[n]] = value
                })
            }
        })
        return keys
    }
    const transpose = m => [...Array(m.reduce((v, r) => (Math.max(v, r.length)), 0)).keys()].map((x, i) => m.map(x => x[i]))
    const hasKeys = (dict, keys) => {
        if (keys.length >= 1 && typeof dict === 'object' && dict.hasOwnProperty(keys[0])) {
            if (keys.length > 1)
                return hasKeys(dict[keys[0]], keys.slice(1))
            return true
        }
    }
    const ravel = arr => Array.isArray(arr) ? arr.reduce((r, v) => r.concat(ravel(v)), []) : [arr]
    const refFilters = {
        vector: ravel,
        idict: arr => {
            let d = {}
            arr.forEach((v, i) => {
                d[i + 1] = v
            })
            return d
        },
        empty: v => Object.keys(v).length ? v : null
    }
    const readReference = (ref, wb, sheet) => {
        if ((typeof ref) !== 'string')
            return ref
        let found = /^\s*(([^!]+)?)?\s*#\s*(([^!]+)?!)?\s*(([A-Z]+|_|\^)\s*(\d+|_|\^)\s*(\(\s*(L|U|R|D|LD|LU|UL|UR|RU|RD|DL|DR)\s*\))?)\s*(:\s*([A-Z]+|_|\^|\.)\s*(\d+|_|\^|\.)\s*(\(\s*(L|U|R|D|LD|LU|UL|UR|RU|RD|DL|DR)\s*\))?)?\s*(:\s*([LURD]+))?\s*(?:\s*(:?[\[{].*[\]}])\s*)?\s*$/gmi.exec(ref)
        if (found) {
            let d = {
                file: found[2],
                sheet: found[4],
                st_col: found[6],
                st_row: found[7],
                st_mov: found[9],
                nd_col: found[11],
                nd_row: found[12],
                nd_mov: found[14],
                range_exp: found[16],
                filters: found[17]
            }
            d.nd_col = d.nd_col || d.st_col
            d.nd_row = d.nd_row || d.st_row
            if ((d.filters || '').startsWith(':')) { // old ref.
                d.filters = null
                if (d.nd_col === d.nd_row && d.nd_col === '.' && d.nd_mov) {
                    d.range_exp = d.nd_mov + (d.range_exp || '')
                    d.nd_mov = null
                }
            }
            let exp = ['L', 'U', 'R', 'D'].map(v => ((d.range_exp || '').split(v).length - 1)),
                filters = JSON.parse(d.filters || '[]');
            if (d.st_mov || d.nd_mov || d.file || [d.st_col, d.st_row, d.nd_col, d.nd_row].some(v => '^_'.includes(v)) || exp.some(v => v > 1) || filters.some(v => !filters.includes(v))) {
                throw new Error('Reference (' + ref + ') not supported!')
            }
            let table, ws = wb.Sheets[d.sheet || sheet],
                range = XLSX.utils.decode_range((d.st_col + d.st_row + ':' + (d.nd_col === '.' ? d.st_col : d.nd_col) + (d.nd_row === '.' ? d.st_row : d.nd_row)).toUpperCase());
            exp = exp.map((n, i) => (i <= 1 ? -n : n))
            while (true) {
                range.s.c += exp[0]
                range.s.r += exp[1]
                range.e.c += exp[2]
                range.e.r += exp[3]
                table = XLSX.utils.sheet_to_json(ws, {header: 1, range})
                if (exp.every(v => v === 0))
                    break
                let flag = exp[1]
                while (flag && table[0].every(v => (v === undefined || v === null))) {
                    table = table.slice(1)
                    range.s.r += 1
                    flag += 1
                    exp[1] = 0
                }
                flag = exp[3]
                while (flag && table[table.length - 1].every(v => (v === undefined || v === null))) {
                    table = table.pop()
                    range.e.r -= 1
                    flag -= 1
                    exp[3] = 0
                }
                if (exp[0] || exp[2]) {
                    table = transpose(table)
                    flag = exp[0]
                    while (flag && table[0].every(v => (v === undefined || v === null))) {
                        table = table.slice(1)
                        range.s.c += 1
                        flag += 1
                        exp[0] = 0
                    }
                    flag = exp[2]
                    while (flag && table[table.length - 1].every(v => (v === undefined || v === null))) {
                        table = table.pop()
                        range.e.c -= 1
                        flag -= 1
                        exp[2] = 0
                    }
                }
            }
            return filters.reduce((r, f) => refFilters[f](r), table)
        }
        return ref
    }
    const parseBook = wb => {
        let res = {}, errors = [];
        wb.SheetNames.forEach(sheet_name => {
            let match = filterMatch(matchSheetName(sheet_name.trim()));
            if (!match) {
                errors.push({
                    type: 'debug',
                    msg: "Sheet name '" + sheet_name + "' cannot be parsed!"
                })
            } else {
                match = Object.assign({
                    scope: 'base',
                    usage: 'input'
                }, match);
                let ws = wb.Sheets[sheet_name], keys, values, data = {},
                    table = XLSX.utils.sheet_to_json(ws, {header: 1});
                if (match.type !== 'mt')
                    table = table.slice(1)
                table = transpose(dropNulls(table));
                match.type = getSheetType(match)
                if (match.type === 'ts') {
                    keys = Object.keys(table)
                    keys = keys.filter((v, i) => '' + v === '' + (i + Number(keys[0])))
                    values = keys.map(k => table[k].slice(1));
                    keys = keys.map(k => table[k][0]);
                } else if (match.type === 'mt') {
                    keys = Object.keys(table).filter(v => v > 1 && table[v][0]);
                    keys = keys.filter((v, i) => '' + v === '' + (i + Number(keys[0])));
                    values = keys.map(k => table[k].slice(1));
                    keys = keys.map(k => (table[1] || []).slice(1).map(v => v ? v + '.' + table[k][0] : null));
                    keys = keys.reduce((r, a) => r.concat(a), []);
                    values = values.reduce((r, a) => r.concat(a), []);
                    values = values.map(v => (readReference(v, wb, sheet_name)))
                } else {
                    keys = table[1] || [];
                    values = (table[2] || []).map(v => (readReference(v, wb, sheet_name)))
                }
                values.forEach((v, i) => {
                    let key = keys[i];
                    if (key && !ravel(v).every(e => (e === undefined || e === null)))
                        data[key] = v
                });
                keys = parseValues(
                    data, match, "in sheet '" + sheet_name + "'", res,
                    errors
                ).map(v => (v.join('.')))
                let times = keys.find(v => v.endsWith('.times'));
                if (match.type === 'ts' && match.scope === 'base' && times) {
                    times = times.split('.').reduce((d, k) => d[k], res);
                    new Set(keys.filter(v => (v.startsWith('base.target.'))).map(v => (v.split('.').slice(0, -1).join('.')))).forEach(k => {
                        k = k + '.times'
                        if (!keys.includes(k)) {
                            k = k.split('.')
                            let d = k.slice(0, -1).reduce((_, i) => _[i], res);
                            k[1] = match.usage
                            if (keys.includes(k.join('.'))) {
                                d['times'] = k.reduce((d, i) => d[i], res)
                            } else {
                                d['times'] = times
                            }
                        }
                    })
                }
            }
        })
        Object.keys(res.base).filter(k => (k !== 'target')).forEach(usage => {
            Object.values(res.base[usage]).forEach(dStage => {
                Object.entries(dStage).forEach(([cycle, data]) => {
                    if (!data.hasOwnProperty('cycle_type'))
                        data.cycle_type = cycle.split('_')[0]
                    data.cycle_type = data.cycle_type.toUpperCase()
                    if (!data.hasOwnProperty('cycle_name'))
                        data.cycle_name = cycle
                    data.cycle_name = data.cycle_name.toUpperCase()
                });
            });
        });
        res.parsing_errors = errors
        return res
    }
    const formatBaseData = base => {
        let res = {}
        Object.entries(base).forEach(([usage, dUsage]) => {
            Object.entries(dUsage).forEach(([stage, dStage]) => {
                Object.entries(dStage).forEach(([cycle, data]) => {
                    res[[usage, stage, cycle].join('.')] = data
                });
            });
        });
        return res
    }
    const get = (d, k, dfl) => (d.hasOwnProperty(k) ? d[k] : dfl)
    const replacer = (key, value) => {
        if (value == null || value.constructor != Object) {
            return value
        }
        return Object.keys(value).sort().reduce((s, k) => {
            s[k] = value[k];
            return s
        }, {})
    }
    const filterObject = (obj, filter) => {
        let res = {};
        Object.keys(obj).filter(filter).forEach(k => {
            res[k] = obj[k]
        });
        return res
    }
    const getDiceReport = (flag, dice, base, schema, timestamp, DICE_version) => {
        const vehicleKeys = [
            'fuel_type', 'engine_capacity', 'gear_box_type',
            'engine_is_turbo', 'engine_max_power',
            'engine_speed_at_max_power',
            'service_battery_delta_state_of_charge',
            'drive_battery_delta_state_of_charge'
        ]
        let vehicle = {}, declared = {}, corrected = {}, ratios = {},
            keys = ['h', 'l'];
        Object.keys(base).forEach(k => {
            let cycle = k.split('.').slice(-1)[0], v = base[k];
            if (k.startsWith('input.calibration')) {
                vehicle[cycle] = filterObject(v, i => (vehicleKeys.includes(i)))
            } else if (k.startsWith('input.prediction') && !vehicle.hasOwnProperty(cycle)) {
                vehicle[cycle] = filterObject(v, i => (vehicleKeys.includes(i)))
            }
            let d = vehicle[cycle]
            if (d && !(d.hasOwnProperty('engine_max_power')) && !(d.hasOwnProperty('engine_speed_at_max_power')) && v.full_load_powers && v.full_load_speeds) {
                let i = ravel(v.full_load_powers).reduce((a, b, i) => a[0] < b ? [b, i] : a, [Number.MIN_VALUE, -1])
                if (i[1] >= 0) {
                    d.engine_max_power = i[0]
                    d.engine_speed_at_max_power = ravel(v.full_load_speeds)[i[1]]
                }
            }
            if (k.startsWith('target.prediction')) {
                if (v.hasOwnProperty('declared_co2_emission_value'))
                    declared[cycle] = v.declared_co2_emission_value
                if (v.hasOwnProperty('corrected_co2_emission_value'))
                    corrected[cycle] = v.corrected_co2_emission_value
            }
        })
        keys.forEach(k => {
            let i = 'wltp_' + k, j = 'nedc_' + k;
            if (declared.hasOwnProperty(i) && declared.hasOwnProperty(j))
                ratios['declared_wltp_' + k + '_vs_declared_nedc_' + k] = declared[i] / declared[j]
            if (declared.hasOwnProperty(i) && corrected.hasOwnProperty(i))
                ratios['declared_wltp_' + k + '_vs_corrected_wltp_' + k] = declared[i] / corrected[i]
        })
        return {
            info: {
                vehicle_family_id: dice.vehicle_family_id,
                CO2MPAS_version: null,
                JET_version: JET_version,
                DICE_version: DICE_version,
                datetime: timestamp,
                SCHEMA_version: schema.title.split('-').slice(-1)[0],
                INPUT_version: flag.input_version
            },
            vehicle,
            ratios
        }
    }
    const json_dump = data => (JSON.stringify(data, replacer, 1).replace(/,\n\s+/g, ', ').replace(/\n\s*/g, ''))
    const define_ta_id = (base, dice, dice_report, meta, encrypted_data, excel_input, errors, signKey) => {
        let ta_id = {
            co2mpas: false,
            vehicle_family_id: dice.vehicle_family_id,
            parent_vehicle_family_id: get(dice, 'parent_vehicle_family_id', ''),
            broken_submission_receipt: get(dice, 'broken_submission_receipt', ''),
            hash: {
                inputs: make_hash(json_dump(base)),
                input: make_hash(json_dump(filterObject(base, k => (k.startsWith('input.'))))),
                target_wltp: make_hash(json_dump(filterObject(base, k => (k.startsWith('target.') && k.includes('wltp'))))),
                target_nedc: make_hash(json_dump(filterObject(base, k => (k.startsWith('target.') && k.includes('nedc'))))),
                meta: make_hash(json_dump(meta)),
                dice: make_hash(json_dump(dice)),
                dice_report: make_hash(json_dump(dice_report)),
                encrypted_data: make_hash(json_dump(encrypted_data)),
                input_file: make_hash(forge.util.createBuffer(excel_input).getBytes()),
            },
            user_random: getRandom99(),
            extension: get(dice, 'extension', 0) ? 1 : 0,
            input_type: get(dice, 'input_type', 'Pure ICE'),
            bifuel: get(dice, 'bifuel', 0) ? 1 : 0,
            wltp_retest: get(dice, 'wltp_retest', '-'),
            comments: get(dice, 'comments', ''),
            atct_family_correction_factor: get(dice, 'atct_family_correction_factor', 1),
            fuel_type: base['input.calibration.wltp_h']['fuel_type'],
            dice: dice,
            validation_errors: errors,
            pub_sign_key: forge.pki.publicKeyToPem(forge.pki.setRsaPublicKey(signKey.n, signKey.e))
        }
        ta_id.signature = sign_data(signKey, json_dump(ta_id))
        return ta_id
    }
    const save_data = data => {
        let tar = new Tar(), i, length, out = '', buf = [];
        Object.keys(data || {}).forEach(k => {
            buf = tar.append(k, jsyaml.safeDump(data[k], {condenseFlow: true}))
        })
        for (i = 0, length = buf.length; i < length; i += 1) {
            out += String.fromCharCode(buf[i]);
        }
        return pako.gzip(out)
    }
    const write_ta_file = (base_name, ta_id, dice_report, encrypted_data, excel_input) => {
        let zip = new JSZip(),
            data = {
                ta_id,
                dice_report,
                encrypted_data
            },
            ta_hash = make_hash(json_dump(data));
        zip.file(base_name + '.input.xlsx', excel_input);
        zip.file(base_name + '.ta', save_data(data));
        zip.file(base_name + '.hash.txt', ta_hash);
        return zip
    }
    const padLeft = num => {
        var len = (String(10).length - String(num).length) + 1;
        return len > 0 ? new Array(len).join('0') + num : num;
    }
    const formatDate = d => (d.getUTCFullYear() + "/" + padLeft(d.getUTCMonth() + 1) + "/" + padLeft(d.getUTCDate()) + "-" + padLeft(d.getUTCHours()) + ":" + padLeft(d.getUTCMinutes()) + ":" + padLeft(d.getUTCSeconds()));
    const mean = x => (x.reduce((s, v) => (s + v), 0) / x.length)
    const std = (x, m) => (Math.sqrt(mean(x.map(v => Math.pow(v - m, 2)))))
    const mean_reject_outliers = x => {
        let m = mean(x), s = std(x, m), y = x.filter(v => s > Math.abs(v - m));
        if (y.length > 2)
            m = mean(y)
        return m
    }
    const calculateEnergy = data => {
        if (data.hasOwnProperty('velocities') && data.hasOwnProperty('times') && data.hasOwnProperty('f0') && data.hasOwnProperty('f1') && data.hasOwnProperty('f2') && data.hasOwnProperty('test_mass')) {
            let velocities = data.velocities,
                times = data.times,
                f0 = data.f0,
                f1 = data.f1,
                f2 = data.f2,
                m = data.test_mass * 1.03;
            return velocities.slice(1).reduce((energy, velocity, index) => {
                let v = (velocities[index] + velocity) / 2,
                    dt = times[index + 1] - times[index],
                    a = (velocity - velocities[index]) / dt / 3.6,
                    f = f0 + v * f1 + v * v * f2 + m * a;
                return energy + (f <= 0 ? 0 : f * v / 3.6 * dt)
            }, 0)
        } else {
            return undefined
        }
    }
    const compileSchema = schema => {
        const ajv = new Ajv({allErrors: true, $data: true});
        ajv.addKeyword('order', {
            validate: function vOrder(schema, data) {
                let func = schema === 'asc' ? (x, y) => (x >= y) : (x, y) => (x <= y)
                if (!data.every((x, i) => (i === 0 || func(x, data[i - 1])))) {
                    vOrder.errors = [{
                        keyword: 'order',
                        message: `should be ${schema} ordered.`,
                        params: {keyword: 'order'}
                    }];
                    return false;
                }
                return true
            }
        });
        ajv.addKeyword('willans_check', {
            validate: function willansCheck(values, data, parent_schema, current_data_path, parent_data) {
                let engine_type = parent_data.ignition_type, value, errors = [];
                if (engine_type === 'positive')
                    engine_type += parent_data.engine_is_turbo ? ' turbo' : ' natural aspiration'
                value = ((values || {}) [parent_data.fuel_type] || {})[engine_type]
                if (value !== undefined && data !== value) {
                    errors.push({
                        keyword: 'willans_check',
                        message: `'${current_data_path}' should be equal to ${value}.`,
                        params: {keyword: 'willans_check'}
                    })
                }
                if (errors.length)
                    willansCheck.errors = errors;
                return errors.length === 0
            }
        });
        ajv.addKeyword('sign_alternator_currents', {
            $data: true,
            validate: function sign_alternator_currentsCheck(b_c, a_c, parent_schema, current_data_path) {
                let errors = [];
                if (mean_reject_outliers(a_c) > 1) {
                    errors.push({
                        keyword: 'sign_alternator_currents',
                        message: `Probably '${current_data_path}' has the wrong sign!`,
                        params: {keyword: 'sign_alternator_currents'}
                    })
                }
                if (errors.length)
                    sign_alternator_currentsCheck.errors = errors;
                return errors.length === 0
            }
        });
        ajv.addKeyword('sign_battery_currents', {
            $data: true,
            validate: function sign_battery_currentsCheck(a_c, b_c, parent_schema, current_data_path) {
                let a_s = mean_reject_outliers(a_c) <= 1,
                    c = cov(a_c, b_c)[0][1], b_s = !a_s, errors = [];
                if (c < 0) {
                    b_s = a_s
                } else if (c === 0) {
                    if (b_c.some(v => v !== 0)) {
                        b_s = mean_reject_outliers(b_c) <= 0
                    } else {
                        b_s = true
                    }
                }
                if (!b_s) {
                    errors.push({
                        keyword: 'sign_battery_currents',
                        message: `Probably '${current_data_path}' has the wrong sign!`,
                        params: {keyword: 'sign_battery_currents'}
                    })
                }
                if (errors.length)
                    sign_battery_currentsCheck.errors = errors;
                return errors.length === 0
            }
        });
        ajv.addKeyword('co2_declared_check', {
            validate: function co2_declaredCheck(coeff, data, parent_schema, current_data_path, parent_data, property_name_parent_data, root_data) {
                let path = current_data_path.split('.'),
                    key = path[path.length - 1].replace('declared_', 'corrected_'),
                    meta = root_data.meta || {}, errors = [],
                    cycle = path[path.length - 2], value,
                    values = [
                        parent_data[key],
                        (meta[cycle + '.test_b.target'] || {})[key],
                        (meta[cycle + '.test_c.target'] || {})[key]
                    ].filter(v => (v !== undefined));

                if (values.length) {
                    value = values.reduce((r, v) => (r + v), 0) / values.length / coeff[values.length - 1]
                    if (value > data) {
                        errors.push({
                            keyword: 'co2_declared_check',
                            message: `'${current_data_path}' should be greater than or equal to ${value}.`,
                            params: {keyword: 'co2_declared_check'}
                        })
                    }
                }
                if (errors.length)
                    co2_declaredCheck.errors = errors;
                return errors.length === 0
            }
        });
        ajv.addKeyword('t1_map_check', {
            $data: true,
            validate: function t1MapCheck(value, data, parent_schema, current_data_path) {
                let errors = [];
                if (value.hasOwnProperty('engine_speed_at_max_power') && value.hasOwnProperty('engine_max_power') && data.hasOwnProperty('full_load_speeds') && data.hasOwnProperty('full_load_powers')) {
                    let ref_speed = value.engine_speed_at_max_power,
                        ref_power = value.engine_max_power,
                        speeds = data.full_load_speeds,
                        powers = data.full_load_powers,
                        n = speeds.length - 1,
                        index = speeds[n] === ref_speed ? n : speeds.findIndex(function (number) {
                            return number > ref_speed;
                        });
                    if (!(0 < index && index < speeds.length)) {
                        errors.push({
                            keyword: 't1_map_check',
                            message: `${current_data_path}/full_load_speeds should contain ${ref_speed}`,
                            params: {keyword: 'full_load_speeds'}
                        })
                    } else if (Math.round(Math.abs((powers[index - 1] * (speeds[index] - ref_speed) + powers[index] * (ref_speed - speeds[index - 1])) / (speeds[index] - speeds[index - 1]) / ref_power - 1) * 100) > 2) {
                        errors.push({
                            keyword: 't1_map_check',
                            message: `${current_data_path}/full_load_powers should contain at ${ref_speed} RPM a value between ${ref_power * .98} - ${ref_power * 1.02} kW`,
                            params: {keyword: 'full_load_powers'}
                        })
                    }
                    if (errors.length)
                        t1MapCheck.errors = errors;
                }
                return errors.length === 0
            }
        });
        ajv.addKeyword('energy_lower_check', {
            $data: true,
            validate: function energyLowerCheck(value, data, parent_schema, current_data_path) {
                let errors = [],
                    e_l = calculateEnergy(data),
                    e_h = calculateEnergy(value);

                if (e_h !== undefined && e_l !== undefined && e_h < e_l) {
                    errors.push({
                        keyword: 'energy_lower_check',
                        message: `${current_data_path} should have an lower energy demand than ${parent_schema['energy_lower_check']['$data'].slice(2)}`,
                        params: {keyword: 'road_loads'}
                    })
                    if (errors.length)
                        energyLowerCheck.errors = errors;
                }
                return errors.length === 0
            }
        });
        ajv.addKeyword('depleting_cycle_time', {
            $data: true,
            validate: function depleting_time_lengthCheck(data, time, parent_schema, current_data_path) {
                let errors = [], cycle = current_data_path.slice(7, 13),
                    tci = data.target.prediction[cycle].transition_cycle_index,
                    tc = data.input.calibration[cycle].times.slice(-1)[0];
                if (time.slice(-1)[0] < tc * tci - 100) {
                    errors.push({
                        keyword: 'depleting_time_length',
                        message: `The '${current_data_path}' has not the all depleting cycles!`,
                        params: {keyword: 'depleting_time_length'}
                    })
                }
                if (errors.length)
                    depleting_time_lengthCheck.errors = errors;
                return errors.length === 0
            }
        });
        return ajv.compile(schema)
    }
    const end = (startTime) => (Math.round((performance.now() - startTime) / 10) / 100)
    const clearInputFile = (input) => {
        try {
            input.value = ''
        } catch (err) {
        }
        if (!/safari/i.test(navigator.userAgent)) {
            input.type = ''
            input.type = 'file'
        }
    }
    const encrypt = (DICE_version, secretPEM, serverPEM, associatedDataHex, signKey, excel_input, schema_raw, timestamp, logMessage, delay) => {
        const secretKey = forge.pki.publicKeyFromPem(secretPEM)
        const serverKey = forge.pki.publicKeyFromPem(serverPEM)
        const associated_data = forge.util.hexToBytes(associatedDataHex)
        timestamp = timestamp || formatDate(new Date());
        const log = val => {
            logMessage('info', val.msg);
            return new Promise(resolve => setTimeout(() => resolve(val.res), delay))
        }
        return Promise.all([
            log({msg: 'Parsing User Signature Key...'}).then(() => {
                const startTime = performance.now();
                if (typeof signKey === 'string') {
                    signKey = JSON.parse(signKey);
                    signKey = forge.pki.decryptRsaPrivateKey(
                        signKey.key, signKey.password || 'co2mpas'
                    );
                }
                if (!signKey)
                    reject("Invalid User Signature Key")
                return {
                    res: signKey,
                    msg: 'User Signature Key parsed in ' + end(startTime) + ' s!'
                }
            }).then(log),
            Promise.all([
                log({msg: 'Parsing Schema...'}).then(() => {
                    const startTime = performance.now();
                    const schema = deref(schema_raw);
                    const validate = compileSchema(schema);
                    return {
                        res: {validate, schema},
                        msg: 'Schema parsed in ' + end(startTime) + ' s!'
                    }
                }).then(log),
                log({msg: 'Parsing XLSX file...'}).then(() => {
                    const startTime = performance.now();
                    const data = parseBook(XLSX.read(excel_input, {type: 'array'}));
                    return {
                        res: data,
                        msg: 'XLSX file parsed in ' + end(startTime) + ' s!'
                    }
                }).then(log).then(data => {
                    data.parsing_errors.forEach(e => logMessage(e.type, e.msg))
                    return data
                })]).then(([{validate, schema}, data]) => {
                return {
                    res: {validate, schema, data},
                    msg: 'Validating XLSX file...'
                }
            }).then(log).then(({validate, schema, data}) => {
                const startTime = performance.now();
                validate(data);
                const errors = validate.errors
                return {
                    res: {data, errors, schema},
                    msg: 'XLSX file validated in ' + end(startTime) + ' s!'
                }
            }).then(log)
        ]).then(([signKey, {data, errors, schema}]) => {
            if (errors)
                throw new Error('There are the following errors in the XLSX file:\n\n' + JSON.stringify(errors, replacer, 2))
            return {
                res: {schema, data, errors, signKey},
                msg: 'Encrypting TA data...'
            }
        }).then(log).then(({schema, data, errors, signKey}) => {
            let startTime = performance.now();
            const meta = data.meta || {};
            const dice = data.dice || {};
            const flag = data.flag || {};
            const data2encrypt = [data.base || {}, meta];
            const base = formatBaseData(data.base || {});
            const dice_report = getDiceReport(flag, dice, base, schema, timestamp, DICE_version);
            const encrypted_data = encrypt_data(data2encrypt, secretKey, serverKey, associated_data);
            const ta_id = define_ta_id(base, dice, dice_report, meta, encrypted_data, excel_input, errors, signKey);
            return {
                res: {ta_id, dice_report, encrypted_data},
                msg: 'Encrypted TA data in ' + end(startTime) + ' s!\nWriting TA (' + ta_id.vehicle_family_id + ') file...'
            }
        }).then(log).then(({ta_id, dice_report, encrypted_data}) => {
            let startTime = performance.now();
            const base_name = timestamp.replace('-', '_').replace(/[\/:]/g, '') + '-' + ta_id.vehicle_family_id + '.jet';
            const ta_file = write_ta_file(base_name, ta_id, dice_report, encrypted_data, excel_input);
            return Promise.all([ta_file.generateAsync({type: "blob"}), {
                base_name,
                startTime
            }])
        }).then(([blob, {base_name, startTime}]) => {
            let fileName = base_name + '.zip',
                href = URL.createObjectURL(blob);
            return {
                res: {href, fileName},
                msg: 'TA file written in ' + end(startTime) + ' s!'
            }
        }).then(log)
    }

    const run = (DICE_version, secretPEM, serverPEM, associatedDataHex, schema) => {
        const button = document.getElementById('run')
        const buttonTextElement = document.getElementById('run-text')
        const buttonText = buttonTextElement.innerHTML
        button.disabled = true
        buttonTextElement.innerHTML = 'Encrypting...'
        const startTime = performance.now();
        const timestamp = formatDate(new Date())
        const signFile = document.getElementById('sign')
        const xlsxFile = document.getElementById('input')
        const consoleDiv = document.getElementById('console')
        const errorsDiv = document.getElementById('errors')
        const downloadLink = document.getElementById('download_encrypted')
        const logsLink = document.getElementById('download_log')
        downloadLink.hidden = true;
        logsLink.hidden = true;
        consoleDiv.textContent = '';
        errorsDiv.textContent = '';
        let consoleLogs = [], errorsLogs = [];
        const log = (msg, type) => {
            let div, className = 'console-log is-' + (type || 'info');
            if (type && type.startsWith('error')) {
                div = errorsDiv
                errorsLogs.push({type, msg})
            } else {
                div = consoleDiv
                consoleLogs.push({type, msg})
            }
            msg.split('\n').forEach(v => {
                let e = document.createElement("div")
                e.className = className
                e.appendChild(document.createTextNode(v.replace(/ /g, '\u00A0')))
                div.appendChild(e)
            })
        }
        const logMessage = (type, message) => {
            if (type === 'error' || type === 'success') {
                button.disabled = false
                buttonTextElement.innerHTML = buttonText
                if (type === 'error') {
                    if ((typeof message) !== 'string')
                        message = message.name + ': ' + message.message
                    log(message, 'error')
                    log('Exited in ' + end(startTime) + ' s!\nAn error has occurred; please correct the inputs accordingly.')
                } else {
                    log(message, type)
                }
                logsLink.href = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify({
                    console: consoleLogs,
                    errors: errorsLogs
                }));
                logsLink.download = timestamp.replace('-', '_').replace(/[\/:]/g, '') + '-jet-logs.json';
                logsLink.hidden = false
            } else {
                log(message, type)
            }
        }
        logMessage('info', 'timestamp ' + timestamp)
        logMessage('info', 'DICE_version ' + (DICE_version || 'unknown'))
        logMessage('info', 'JET_version ' + JET_version)
        logMessage('info', 'Schema_version ' + (schema.title || 'unknown-').split('-').slice(-1)[0])

        if (!signFile.value) {
            logMessage('error', 'User Signature Key is Required!')
        } else if (!xlsxFile.value) {
            logMessage('error', 'DICE .xlsx File is Required!')
        } else {
            logMessage('log', 'Loading files...')
            Promise.all([performance.now(), new Promise((resolve, reject) => {
                let reader = new FileReader();
                reader.onerror = () => {
                    clearInputFile(signFile)
                    reject('User Signature Key cannot be loaded. Please select again the file.')
                };
                reader.onload = () => resolve(reader.result);
                reader.readAsText(signFile.files[0]);
            }), new Promise((resolve, reject) => {
                let reader = new FileReader();
                reader.onerror = () => {
                    clearInputFile(xlsxFile)
                    reject('DICE .xlsx File cannot be loaded. Please select again the file.');
                };
                reader.onload = () => resolve(reader.result);
                reader.readAsArrayBuffer(xlsxFile.files[0]);
            })]).then(([startTime, sign, xlsx]) => {
                logMessage('log', 'Files loaded in ' + end(startTime) + ' s!')
                return encrypt(DICE_version, secretPEM, serverPEM, associatedDataHex, sign, xlsx, schema, timestamp, logMessage, 100)
            }).then(({href, fileName}) => {
                downloadLink.href = href;
                downloadLink.download = fileName;
                downloadLink.hidden = false;
                logMessage('success', 'Done in ' + end(startTime) + ' s!')
                downloadLink.click()
            }).catch((e) => logMessage('error', e))
        }
    }
    const onChange = () => {
        document.getElementById('download_encrypted').hidden = true
        document.getElementById('download_log').hidden = true
        document.getElementById('console').textContent = ''
        document.getElementById('errors').textContent = ''
    }
    module.exports = {__version__: JET_version, run, onChange}
}());