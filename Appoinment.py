# ITE 260 - COMPUTER PROGRAMMING 1
# PERIOD 2 PROJECT
# DOCTOR & CLINIC APPOINTMENT SCHEDULER

from datetime import datetime, timedelta


# DATA STORAGE

# List of available doctors
doctors = [
    "Dr. Magdaleno, Diwanie",
    "Dr. Lawagon Karl",
    "Dr. Pantao, Sodais"
]

# List of appointment records
appointments = []

# Starting appointment ID
next_id = 1

# Clinic hours (8:00 AM - 5:00 PM)
CLINIC_OPEN = datetime.strptime("08:00 AM", "%I:%M %p").time()
CLINIC_CLOSE = datetime.strptime("05:00 PM", "%I:%M %p").time()

# Cancellation rule: must cancel at least this many days before the appointment
CANCEL_NOTICE_DAYS = 3


# FUNCTION: DISPLAY DOCTORS

def display_doctors():
    """Display all available doctors."""

    print("\n AVAILABLE DOCTORS ")

    for index, doctor in enumerate(doctors, start=1):
        print(f"{index}. {doctor}")


# FUNCTION: PARSE TIME

def parse_time(time_text):
    """
    Convert a time like '9:00 AM' into a standard '09:00 AM' string.
    Returns None if the format is invalid.
    """

    try:
        parsed = datetime.strptime(time_text.strip().upper(), "%I:%M %p")
        return parsed.strftime("%I:%M %p")
    except ValueError:
        return None


# FUNCTION: CHECK CLINIC HOURS

def is_within_clinic_hours(time_text):
    """Check if a standardized time (HH:MM AM/PM) is within clinic hours."""

    chosen = datetime.strptime(time_text, "%I:%M %p").time()

    return CLINIC_OPEN <= chosen <= CLINIC_CLOSE


# FUNCTION: GET APPOINTMENT DATE AND TIME

def get_appointment_datetime(date, time):
    """Combine the date (YYYY-MM-DD) and time (HH:MM AM/PM) into one datetime."""

    return datetime.strptime(f"{date} {time}", "%Y-%m-%d %I:%M %p")


# FUNCTION: AUTOMATIC SUCCESSFUL BOOKING NOTICE

def check_completed_appointments():
    """
    Check every scheduled appointment. If its date and time has
    arrived, automatically mark it as Successful and announce it.
    """

    now = datetime.now()

    for appointment in appointments:

        if appointment["status"] != "Scheduled":
            continue

        appointment_time = get_appointment_datetime(
            appointment["date"], appointment["time"]
        )

        if now >= appointment_time:
            appointment["status"] = "Successful"

            print("\n" + "=" * 40)
            print(" BOOKING SUCCESSFUL!")
            print(f" Appointment ID: {appointment['id']}")
            print(f" Patient: {appointment['patient']}")
            print(f" Doctor: {appointment['doctor']}")
            print(f" Date: {appointment['date']}")
            print(f" Time: {appointment['time']}")
            print(" The scheduled date and time has arrived.")
            print("=" * 40)


# FUNCTION: VIEW DOCTOR'S APPOINTMENTS

def view_doctor_appointments():
    """Display all appointments for a selected doctor."""

    print("\n VIEW DOCTOR'S APPOINTMENTS ")

    # Display doctors
    display_doctors()

    # Validate doctor selection
    while True:
        try:
            doctor_choice = int(input("Select doctor number: "))

            if doctor_choice >= 1 and doctor_choice <= len(doctors):
                doctor = doctors[doctor_choice - 1]
                break
            else:
                print("Invalid doctor number.")

        except ValueError:
            print("Please enter a valid number.")

    print(f"\nAppointments for {doctor}")

    found = False

    for appointment in appointments:

        if appointment["doctor"] == doctor:
            print(f"\nAppointment ID: {appointment['id']}")
            print(f"Patient: {appointment['patient']}")
            print(f"Date: {appointment['date']}")
            print(f"Time: {appointment['time']}")
            print(f"Status: {appointment['status']}")
            found = True

    if not found:
        print("No appointments scheduled for this doctor.")


# FUNCTION: VALIDATE DATE

def validate_date(date):
    """Check if the date is a real date in YYYY-MM-DD format."""

    parts = date.split("-")

    if len(parts) != 3:
        return False

    if len(parts[0]) != 4 or len(parts[1]) != 2 or len(parts[2]) != 2:
        return False

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False

    return True


# FUNCTION: CHECK AVAILABILITY

def check_availability(doctor, date, time):
    """
    Check whether a doctor is already booked
    for the selected date and time.
    """

    for appointment in appointments:
        if (appointment["doctor"] == doctor and
                appointment["date"] == date and
                appointment["time"] == time):

            return False

    return True


# FUNCTION: SCHEDULE APPOINTMENT

def schedule_appointment():
    """Create and save a new appointment."""

    global next_id

    print("\n SCHEDULE APPOINTMENT ")

    patient = input("Enter patient name: ").strip()

    # Validate patient name
    if patient == "":
        print("Error: Patient name cannot be empty.")
        return

    # Display doctors
    display_doctors()

    # Validate doctor selection
    while True:
        try:
            doctor_choice = int(input("Select doctor number: "))

            if doctor_choice >= 1 and doctor_choice <= len(doctors):
                doctor = doctors[doctor_choice - 1]
                break
            else:
                print("Invalid doctor number.")

        except ValueError:
            print("Please enter a valid number.")

    # Get appointment date
    while True:
        date = input("Enter appointment date (YYYY-MM-DD): ").strip()

        if validate_date(date):
            break
        else:
            print("Invalid date. Use a real date in YYYY-MM-DD format.")

    # Get appointment time (must be valid, within clinic hours, not in the past)
    print("\nClinic hours: 8:00 AM - 5:00 PM")

    while True:
        time_input = input("Enter appointment time (example: 09:00 AM): ")
        time = parse_time(time_input)

        if time is None:
            print("Invalid time. Use the format HH:MM AM/PM (example: 09:00 AM).")
            continue

        if not is_within_clinic_hours(time):
            print("Sorry, that time is outside clinic hours.")
            print("Please choose a time between 8:00 AM and 5:00 PM.")
            continue

        if get_appointment_datetime(date, time) <= datetime.now():
            print("That date and time has already passed. Choose a later time.")
            continue

        break

    # Check if schedule is available
    if check_availability(doctor, date, time):

        appointment = {
            "id": next_id,
            "patient": patient,
            "doctor": doctor,
            "date": date,
            "time": time,
            "status": "Scheduled"
        }

        appointments.append(appointment)

        print("\nAppointment successfully scheduled!")
        print(f"Appointment ID: {next_id}")
        print(f"Patient: {patient}")
        print(f"Doctor: {doctor}")
        print(f"Date: {date}")
        print(f"Time: {time}")
        print("Status: Scheduled")
        print("You will be notified once the date and time arrives.")

        next_id += 1

    else:
        print("\nSorry, the doctor is already booked")
        print("for the selected date and time.")


# FUNCTION: SEARCH APPOINTMENT

def search_appointment():
    """Search for an appointment using the patient name."""

    print("\n SEARCH APPOINTMENT ")

    patient_name = input("Enter patient name: ").strip()

    found = False

    for appointment in appointments:

        if appointment["patient"].lower() == patient_name.lower():

            print("\nAppointment Found!")
            print(f"ID: {appointment['id']}")
            print(f"Patient: {appointment['patient']}")
            print(f"Doctor: {appointment['doctor']}")
            print(f"Date: {appointment['date']}")
            print(f"Time: {appointment['time']}")
            print(f"Status: {appointment['status']}")

            found = True

    if not found:
        print("No appointment found for that patient.")


# FUNCTION: CANCEL APPOINTMENT

def cancel_appointment():
    """Cancel an appointment using its ID."""

    print("\n CANCEL APPOINTMENT ")

    if len(appointments) == 0:
        print("There are no appointments to cancel.")
        return

    try:
        appointment_id = int(input("Enter appointment ID: "))

    except ValueError:
        print("Please enter a valid appointment ID.")
        return

    for appointment in appointments:

        if appointment["id"] == appointment_id:

            if appointment["status"] == "Successful":
                print("This appointment is already completed")
                print("and can no longer be cancelled.")
                return

            appointment_time = get_appointment_datetime(
                appointment["date"], appointment["time"]
            )
            deadline = appointment_time - timedelta(days=CANCEL_NOTICE_DAYS)

            if datetime.now() > deadline:
                print(f"\nSorry, appointments can only be cancelled at least")
                print(f"{CANCEL_NOTICE_DAYS} days before the scheduled date.")
                print(f"The cancellation deadline was "
                      f"{deadline.strftime('%Y-%m-%d %I:%M %p')}.")
                return

            appointments.remove(appointment)

            print("\nAppointment successfully cancelled.")
            return

    print("Appointment ID not found.")


# FUNCTION: MAIN MENU

def display_menu():
    """Display the main system menu."""

    print("\n")

    print("      CLINIC APPOINTMENT SYSTEM")
    

    print("1. View Doctors")
    print("2. Choose Appointment")
    print("3. View Doctor's Appointments")
    print("4. Search Appointment")
    print("5. Cancel Appointment")
    print("6. Exit")


# MAIN PROGRAM

def main():

    while True:

        # Automatically announce appointments whose time has arrived
        check_completed_appointments()

        display_menu()

        choice = input("Enter your choice (1-6): ").strip()

        # Check again right after the user responds
        check_completed_appointments()

        if choice == "1":
            display_doctors()

        elif choice == "2":
            schedule_appointment()

        elif choice == "3":
            view_doctor_appointments()

        elif choice == "4":
            search_appointment()

        elif choice == "5":
            cancel_appointment()

        elif choice == "6":
            print("\nThank you for using the Appointment Scheduler!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice.")
            print("Please select a number from 1 to 6.")


# Start the program
main()
