#!/usr/bin/env bash

cd "$(dirname "$0")"
python update_version.py
npm i
rm -r dist
mkdir "dist"
for f in encrypt sign_key
do
 echo "Browserify $f..."
 browserify src/$f.js > dist/$f.js -s $f
 echo "$f.js $(ls -lah dist/$f.js | awk '{ print $5}')"
 echo "Babel & uglifyjs $f..."
 npx babel dist/$f.js --presets=@babel/preset-env | uglifyjs --compress --mangle > dist/$f.min.js
 echo "$f.min.js $(ls -lah dist/$f.min.js | awk '{ print $5}')"
 echo "Moving files $f..."
 cp dist/$f.js ../co2mpas_dice/server/templates/js/$f.js
 cp dist/$f.min.js ../co2mpas_dice/server/templates/js/$f.min.js
 echo "Done $f!"
done