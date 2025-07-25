# ServeSmart

ServeSmart is a mess management solution designed to address food preparation and dining space challenges at IIIT Kottayam. By enabling students to pre-register for meals through a meal token and QR code system, ServeSmart allows admins to accurately track meal attendance, reducing food waste and optimizing resources. Built on a Python full-stack framework, the platform also features real-time data tracking and an admin dashboard for monitoring and managing meal registrations.

## Features

- **User Authentication:** Secure login for students and admins.
- **Meal Token Generation:** Students can generate meal tokens linked to unique QR codes.
- **QR Code Verification:** Admins can scan QR codes to confirm meal registrations.
- **Real-Time Data Tracking:** Track the number of students registering for each meal.
- **Admin Dashboard:** Comprehensive dashboard for monitoring meal registrations.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask, Celery (redis)
- **Database:** MySQL
- **QR Code Generation:** Segno
- **Version Control:** Git, GitHub
- **Containerization:** Docker
## Steps to Execute the Application

1. **Read this README file** to understand the application's functionality and setup process.
2. **Clone the repository** using the following command:
   ```sh
   git clone https://github.com/Chaitan2004/servesmart
   ```
3. **Navigate to the project folder**:
   ```sh
   cd servesmart
   ```
4. **Build and start the Docker containers**:
   ```sh
   docker-compose up --build
   ```
5. **Access the services** via:
   - **Web Application**: [http://localhost:8080](http://localhost:8080)
   
6. **Login Credentials**:
   - **Username**: `2022BCD0038`
   - **Password**: `160M269W`
   
   Use these credentials to access the student dashboard.

7. **Check running containers**:
   ```sh
   docker ps
   ```
   - Containers are prefixed with `2022bcd0038` for the **web service** and **worker service** as per project specifications.

8. **Stop and clean up the application**:
   ```sh
   docker-compose down
   ```

## Notes
- Card history and card registration features are not yet functional.
- Ensure Docker and Docker Compose are installed before running the application.

For any issues, refer to the project repository or contact the development team.

