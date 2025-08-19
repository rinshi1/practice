To set up and run your Python script on different operating systems, follow these step-by-step instructions:

## Common Step: Create the `.env` File

For all systems, first create a `.env` file in the same directory as your script with the following environment variables:

```
DEPLOYMENT_NAME="your_deployment_name"
OPENAI_API_TYPE="openai_api_type"
AZURE_OPENAI_ENDPOINT="https://your-azure-endpoint.openai.com"
OPENAI_API_VERSION="api_version"
AZURE_OPENAI_API_KEY="your_azure_api_key"
```

Replace the placeholder values with your actual credentials and information.

## Windows

1. **Open Command Prompt**: Press `Win + R`, type `cmd`, and press Enter.
2. **Navigate to Script Directory**:
   ```shell
   cd path\to\your\script
   ```
3. **Install Required Packages**:
   ```shell
   python -m venv venv
   venv\Scripts\activate
   pip install python-dotenv langchain_openai langgraph
   ```
4. **Run the Script**:
   ```shell
   python your_script_name.py
   ```

## macOS

1. **Open Terminal**: Press `Cmd + Space`, type `Terminal`, and press Enter.
2. **Navigate to Script Directory**:
   ```bash
   cd /path/to/your/script
   ```
3. **Install Required Packages**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install python-dotenv langchain_openai langgraph
   ```
4. **Run the Script**:
   ```bash
   python3 your_script_name.py
   ```

## Linux

1. **Open Terminal**.
2. **Navigate to Script Directory**:
   ```bash
   cd /path/to/your/script
   ```
3. **Install Required Packages**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install python-dotenv langchain_openai langgraph
   ```
4. **Run the Script**:
   ```bash
   python3 your_script_name.py
   ```

Make sure to replace `your_script_name.py` with the actual name of your Python script file, and adjust the paths to reflect the location of your script and installation environment accordingly.