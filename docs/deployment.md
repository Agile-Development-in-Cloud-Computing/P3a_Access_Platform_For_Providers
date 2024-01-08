# Table of Contents

1. [Introduction to PythonAnywhere](#introduction-to-pythonanywhere)
2. [Deployment Process](#deployment-process)
   - [Creating an Account and Accessing Dashboard](#creating-an-account-and-accessing-dashboard)
   - [Setting Up the Web App](#setting-up-the-web-app)
   - [Accessing web2py Installation](#accessing-web2py-installation)
   - [Preparing Application for Upload](#preparing-application-for-upload)
   - [Uploading the App to PythonAnywhere](#uploading-the-app-to-pythonanywhere)
   - [Completing the Deployment](#completing-the-deployment)
3. [Conclusion](#conclusion)

## Introduction to PythonAnywhere

[PythonAnywhere](https://www.pythonanywhere.com/) is a cloud-based integrated development environment (IDE) designed to assist users in developing, managing, and hosting Python applications online. It offers an intuitive platform for deploying web applications without the complexities of setting up servers. PythonAnywhere supports various frameworks, including web2py, Flask, Django, and more, making it a versatile choice for developers.

## Deployment Process

### Creating an Account and Accessing Dashboard

1. **Create an Account:**
   - Sign up for a PythonAnywhere account, opting for the free "Beginner" account.
   - [Login](#creating-an-account-and-accessing-dashboard) to access the Dashboard.

### Setting Up the Web App

2. **Web App Setup:**
   - Click on the **"Web"** tab within the Dashboard.
   - Select **"Add a new web app"** to begin the setup process.
   - Choose **"web2py"** as the web framework and proceed with the setup.

### Accessing web2py Installation

3. **Accessing web2py:**
   - Enter the admin password as prompted during the setup.
   - After completion, access the web2py installation at **"http://YOUR_USERNAME.pythonanywhere.com/welcome/default/index"**.

### Preparing Application for Upload

4. **Preparing Application:**
   - Access your web2py development machine, typically at **"http://127.0.0.1:8000/admin/default/site"**.
   - Navigate to **"Manage"** and select **"Pack all"** on your application, saving the packed file on your local disk.

### Uploading the App to PythonAnywhere

5. **Uploading the Application:**
   - Open a browser and go to **"https://YOUR_USERNAME.pythonanywhere.com/admin"** (ensure it's HTTPS).
   - Log in using your admin credentials.
   - Find the **"Upload and install packed application"** section.
   - Provide the application name as **"init"**.
   - Select the packed application file saved in step 4 for upload.

### Completing the Deployment

6. **Deployment Completion:**
   - Upon a successful upload, your application will be accessible at **"http://YOUR_USERNAME.pythonanywhere.com/"**.

## Conclusion

PythonAnywhere simplifies the deployment process by providing an accessible platform for hosting web2py applications. By following these steps, users can seamlessly upload their applications and make them available online for users to access.
