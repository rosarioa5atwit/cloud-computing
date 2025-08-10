This project is a FastAPI web service that demonstrates the use of HTTP headers and cookies for authentication, session management, and API security. It includes features such as user signup and login with session cookies, header-based authentication (including API keys and rate limiting), cookie-based preferences (for language and timezone), session management (covering login, logout, and profile access), and rate-limited API endpoints. This lab is designed to help users understand how headers and cookies work in web applications and how to implement them securely in FastAPI.

The key features of this project include user authentication, which allows for user registration and session creation. The `/signup` endpoint lets users register by storing their username and password. The `/login` endpoint is used to authenticate users and create a session, while the `/logout` endpoint invalidates the session and clears cookies.

In terms of session and cookie management, the service stores session IDs in secure, HTTP-only cookies and tracks user preferences (like language and timezone) via cookies. It also validates sessions before granting access to certain features.

Additionally, the project incorporates header-based security measures. The `/api/secure` endpoint is subject to rate limiting, restricting the number of API calls from a single IP address.

To run this program you need to run main.py. Then run driver.py or test_service.py.