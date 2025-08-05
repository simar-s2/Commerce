# 🛍️ Commerce – Django Auction Web Application

**Commerce** is an online auction platform built with **Python (Django)** and a **Bootstrap-based HTML/CSS** front end. It allows users to create and manage auction listings, place bids, and engage in discussions via comments. The project showcases developer Simarjot Singh’s full-stack skills: the backend uses Django and the front end uses Bootstrap for responsive design. Key features include user authentication, listing creation, bidding, commenting, category filtering, and watchlists.

## Features

- **User Accounts:** Secure registration and login (leveraging Django’s built-in auth system)  
- **Auction Listings:** Create, edit, and view auction items (title, description, starting bid, image, category)  
- **Bidding:** Place bids on active listings; the system tracks the current highest bid  
- **Comments:** Leave comments on any listing to discuss items with other users  
- **Watchlist:** Add or remove listings from a personal watchlist for quick access to favorites  
- **Category Filtering:** Browse and filter listings by category (e.g., Fashion, Electronics)  
- **Admin Panel:** Manage all site data (listings, bids, comments) through Django’s admin interface

## Screenshots

*Screenshots coming soon – placeholders shown below.*

![Homepage Screenshot (placeholder)](static/images/auctions.png)  
*Figure 1: Placeholder for the Commerce app homepage*

![Listing Detail (placeholder)](/images/listing_placeholder.png)  
*Figure 2: Placeholder for a listing’s detail page*

## Project Structure

```
Commerce/
├── auctions/             # Main app (models, views, templates, static files)
│   ├── migrations/       # Database migrations
│   ├── templates/        # HTML templates for auction pages
│   ├── static/           # Static files (CSS, JS, images)
│   ├── models.py         # Data models (User, Listing, Bid, Comment)
│   ├── views.py          # View functions and business logic
│   ├── forms.py          # Forms (listing creation, bidding, etc.)
│   └── urls.py           # App URL configurations
├── commerce/             # Django project settings
│   ├── __init__.py
│   ├── settings.py       # Project configuration (settings)
│   ├── urls.py           # Root URL routing
│   └── wsgi.py           # WSGI entry point
├── manage.py             # Django command-line utility
├── db.sqlite3            # SQLite database (development)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Installation

To set up the Commerce project locally:

1. **Clone the repository:**  
   ```bash
   git clone https://github.com/simar-s2/Commerce.git
   cd Commerce
   ```
2. **Create and activate a virtual environment:**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply database migrations:**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Run the development server:**  
   ```bash
   python manage.py runserver
   ```
6. **Access the app:**  
   Open your browser to `http://127.0.0.1:8000/`

## Usage

- **Register/Login:** Create a user account or log in with existing credentials  
- **Create Listings:** Add new auctions with title, description, bid, image, and category  
- **Browse and Bid:** View and bid on active listings  
- **Comment:** Post comments on listings  
- **Watchlist:** Track favorites via a personal watchlist  
- **Admin:** Use Django Admin to manage data

## Future Enhancements

- Add automated unit tests and CI integration
- Include Docker and deployment scripts
- Support image uploads and search functionality
- Add email notifications and real-time bidding updates
- Improve mobile responsiveness and UI components
- Add LICENSE file and contribution guidelines

## License

To be added – recommend MIT License for open source contributions.
