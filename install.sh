python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

path_to_project="$(cd "$(dirname "$1")" && pwd -P)/$(basename "$1")"
python_path="venv/bin/python3"
app_path="app.py"

echo "#! $path_to_project$python_path" > $app_path
echo "from cli import app" >> $app_path
echo "if __name__ == '__main__':" >> $app_path
echo "	app()" >> $app_path

chmod +x app.py

echo "alias sm=$path_to_project$app_path" >> ~/.bashrc
