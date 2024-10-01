# DALL-E Image Playground

DALL-E Image Playground is a web-based application that allows users to interact with OpenAI's DALL-E API. Users can create images from text prompts, edit existing images, and generate variations of uploaded images. This project uses Flask as the backend framework to serve the web application.

## Features

- **Generate Images**: Create AI-generated images by providing a text prompt.
- **Edit Images**: Upload an image and apply modifications using AI.
- **Image Variations**: Generate multiple variations of an uploaded image.

## Demo

You can try out the application locally by following the installation instructions below.

## Installation

### Prerequisites

- **Python 3.8+**: Ensure Python is installed on your system. You can download it [here](https://www.python.org/downloads/).
- **Git**: Ensure Git is installed on your system. You can download it [here](https://git-scm.com/downloads).

### 1. Clone the repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/mahiworld/image-playground.git
```

### 2. Navigate into the project directory

```bash
cd image-playground
```

### 3. Create a virtual environment

It's recommended to create a virtual environment to manage dependencies. Run the following command:

```bash
python3 -m venv hi-venv
```

### 4. Activate the virtual environment

On macOS/Linux:

```bash
source hi-venv/bin/activate
```

On Windows:

```bash
hi-venv\Scripts\activate
```

### 5. Install dependencies

Install the required dependencies using the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 6. Set up environment variables

Create a .env file in the root directory of the project, and add your OpenAI API key:

```makefile
OPENAI_API_KEY=your_openai_api_key_here
```

### 7. Launch the application

To start the Flask development server, run the following command:

```bash
flask run
```

The app will be available at http://127.0.0.1:5000/