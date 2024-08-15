
# CARECONNECT

**CARECONNECT** is a comprehensive medical assistance application designed to offer users 24/7 support through an intelligent chatbot. The app helps users find hospitals, pharmacies, government hospitals, and multi-speciality hospitals, and provides their locations on maps. 

## Features

- **24/7 Chatbot Assistance:** Engage with a chatbot that provides medical assistance and answers user queries.
- **Hospital Finder:** Search for hospitals based on type (e.g., government, multi-speciality) and view their locations on a map.
- **Appointment Scheduling:** Book appointments and receive confirmation details.
- **Location Detection:** Identify and save districts based on user-provided addresses.

## Technologies Used

- **Flask:** Web framework for building the application.
- **MySQL:** Database for storing hospital data.
- **Pandas:** Data manipulation and analysis.
- **NLTK & SentenceTransformers:** Natural language processing and text embedding for chatbot functionality.
- **OpenCage API:** Geocoding API for address location services.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/careconnect.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd careconnect
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    Ensure you have a MySQL server running and create a database named `testdb`. Update the database credentials in the `app.py` file if needed.

5. **Initialize the database:**

    Run the following command to initialize the database with hospital data:

    ```bash
    python app.py
    ```

## Usage

1. **Run the application:**

    ```bash
    python app.py
    ```

2. **Access the application:**
   
    Open your web browser and go to `http://127.0.0.1:5000/`.

3. **Interact with the chatbot:**

    Use the chatbot feature to ask medical-related questions and receive assistance.

4. **Find hospitals and pharmacies:**

    Use the hospital and pharmacy finder to locate and get information about medical facilities.

## API Endpoints

- `/`: Home page.
- `/appointment`: Appointment booking page.
- `/appointment-details`: Displays appointment details.
- `/confirmation`: Confirmation page for appointments.
- `/listofhosp`: Page showing a list of hospitals.
- `/find_district`: API endpoint to find district based on address (POST).
- `/save_district`: API endpoint to save district information (POST).
- `/lab_test`: Lab test information page.
- `/govn_hospitals`: Government hospitals page.
- `/ms_hospitals`: Multi-speciality hospitals page.
- `/chat`: Chat interface for interacting with the chatbot.

## Contributing

We welcome contributions to enhance the CARECONNECT project. If you would like to contribute, please follow these steps:

1. **Fork the repository.**
2. **Create a new branch for your feature or fix:**

    ```bash
    git checkout -b my-feature-branch
    ```

3. **Make your changes and commit them:**

    ```bash
    git add .
    git commit -m "Add new feature or fix"
    ```

4. **Push your branch to your forked repository:**

    ```bash
    git push origin my-feature-branch
    ```

5. **Open a pull request on GitHub.**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenCage** for the geocoding API.
- **NLTK** and **SentenceTransformers** for natural language processing tools.

## Contact

For questions or further information, please contact:

- **Name:** Your Name
- **Email:** your.email@example.com
- **GitHub:** [yourusername](https://github.com/yourusername)

Implementation:
![homepage](https://github.com/user-attachments/assets/1c5b262d-3289-4cd6-8529-925d4ddde901)
![homepage2](https://github.com/user-attachments/assets/76550882-fec3-4227-a236-7fae04ef9d53)
![homepage3](https://github.com/user-attachments/assets/588921b4-55b3-4762-8b0d-bf658e2b767e)
![homepage4](https://github.com/user-attachments/assets/6964b48c-272b-4c28-a003-eae0019c2ccf)
![homepage5](https://github.com/user-attachments/assets/aebf71df-daf7-40d3-8563-e33112d7772e)
![list](https://github.com/user-attachments/assets/6f71c84f-e496-4d9b-88eb-6d45383fb8ae)
![chatbot](https://github.com/user-attachments/assets/d47bb549-df0c-4772-b33b-18873df7dcf5)
