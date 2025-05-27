## Setup Instructions

1. **Create the project directory structure:**
```bash
mkdir qnnotate_jobs
cd qnnotate_jobs
mkdir templates static
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Access the application:**
   - Open your browser and go to `http://127.0.0.1:5000`
   - You'll be redirected to the admin login page

## Usage Guide

### Admin Access:
- **Username:** `gle63s`
- **Password:** `benzo_na_bimmer`

### Admin Features:
1. **Create Users:** Admin can create login credentials for users
2. **Create Tasks:** Add new job postings with title and description
3. **Edit Tasks:** Modify existing task details
4. **View Bids:** See all bids placed on tasks
5. **Assign Tasks:** Select winning bids and assign tasks to users
6. **Mark Complete:** Mark tasks as completed and add payment to user earnings
7. **Delete Tasks:** Remove tasks entirely

### User Features:
1. **Login:** Use credentials created by admin
2. **Browse Jobs:** View all available open tasks
3. **Place Bids:** Submit bid amounts for tasks
4. **Update Bids:** Modify existing bids before task assignment
5. **Track Earnings:** View total earnings prominently displayed
6. **Monitor Bid Status:** See status of all placed bids

### Key Features:
- **Secure Login:** Separate admin and user authentication
- **Bidding System:** Users can bid on tasks with their desired payment
- **Task Management:** Complete lifecycle from creation to completion
- **Earnings Tracking:** Collective earnings display for users
- **Responsive Design:** Works on desktop and mobile devices
- **Status Tracking:** Clear status indicators for tasks and bids

The application uses SQLite database for data storage and includes proper error handling and flash messages for user feedback. The design follows your specified color scheme with `#f2f4f8` as the background and `#0f8a65` as the primary accent color.
