export FUNCTION_NAME=$(basename `pwd`)

zip -r ${FUNCTION_NAME}.zip ./ -x '*.git*'
aws lambda update-function-code --function-name ${FUNCTION_NAME} --zip-file fileb://${FUNCTION_NAME}.zip
rm ./${FUNCTION_NAME}.zip