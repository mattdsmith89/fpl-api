
echo -e "\e[0;36mRemoving dist...\e[0m"
rm -rf dist

echo -e "\e[0;36mCreating dist...\e[0m"
mkdir dist
cd dist

echo -e "\e[0;36mCopying source...\e[0m"
cp -r ../src/* .

echo -e "\e[0;36mInstalling dependencies...\e[0m"
pip3 install requests -t .

echo -e "\e[0;36mCreating lambda archive...\e[0m"
zip -r lambda.zip *

echo -e "\e[0;36mPushing to AWS...\e[0m"
aws lambda update-function-code --function-name fpl_overview --zip-file fileb://lambda.zip

echo -e "\e[0;36mRemoving dist...\e[0m"
cd ..
rm -rf dist