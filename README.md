# Bandersnatch Project

## Introduction
Bandersnatch is a data science and machine learning project that allows you to work with monster data, create visualizations, and build a machine learning model. The project is structured as a series of sprints that build on each other, guiding you through database operations, data visualization, and machine learning model development.

## Project Structure
- `/`: Splash Page
- `/data`: Tabular Monster Data
- `/view`: Dynamic Visualizations
- `/model`: Interactive Machine Learning Model

## Sprint Tickets
Work through these sprints in order:
1. [Sprint 1: Database Operations](tickets/firstTicket.md) - Set up MongoDB and create monster data
2. [Sprint 2: Dynamic Visualizations](tickets/secondTicket.md) - Create interactive visualizations with Altair
3. [Sprint 3: Machine Learning Model](tickets/thirdTicket.md) - Build and integrate a machine learning model

## Getting Started

### Fork and Clone the Repository
1. Fork this repository to your GitHub account
2. Clone your forked repository locally:
```
git clone https://github.com/your-username/BandersnatchStarter.git
cd BandersnatchStarter
```

### Setup Virtual Environment
#### Windows
```
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

#### macOS/Linux
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt
```

Alternatively, macOS/Linux users can use the provided install script:
```
source venv/bin/activate
./install.sh
```

### Running the Application

#### Windows
```
python -m app.main
```

#### macOS/Linux
```
python3 -m app.main
```

Or use the provided run script:
```
./run.sh
```

The application will be available at http://127.0.0.1:5000/

### Deploying to Render.com

1. Create a free account on [Render.com](https://render.com)
2. From your dashboard, click "New" and select "Web Service"
3. Connect your GitHub repository or use the public GitHub URL
4. Configure your web service:
   - Name: Choose a name for your application
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app.main:APP`
5. Add environment variables:
   - Add your MongoDB connection string as `DB_URL`
6. Click "Create Web Service"

Your application will be deployed and available at a URL provided by Render.

## Tech Stack
- Logic: Python3
- API Framework: Flask
- Templates: Jinja2
- Structure: HTML5
- Styling: CSS3
- Database: MongoDB
- Graphs: Altair
- Machine Learning: Scikit
- Hosting: Render.com

## Database Setup (for Sprint 1)
1. Sign up for a MongoDB account: [MongoDB](https://account.mongodb.com)
2. Create a "Shared Cluster" (free tier)
3. Add your IP address to the allowed locales list
4. Copy the connection string into a `.env` file in your project root:
   ```
   DB_URL=mongodb+srv://<username>:<password>@<cluster>.<project_id>.mongodb.net
   ```

## Windows-Specific Notes
- Windows users may need to download the [wheel for fortuna](https://github.com/decagondev/fortuna-bin-win64) dependency and follow its [README](https://github.com/decagondev/fortuna-bin-win64/blob/main/README.md)
- Gunicorn is not Windows compatible, so don't use the `run.sh` script on Windows

## Stretch Goals
- Use ElephantSQL instead of MongoDB
- Use Plotly instead of Altair
- Use PyTorch instead of Scikit
- Use FastAPI instead of Flask
- Add the ability for the user to reset & reseed the database
- Add the ability for the user to re-train the machine learning model
- Add the ability for the user to download a working serialized model and dataset
- Add authentication to sensitive pages
- Use a different set of features to train the model
- Use your own dataset entirely
