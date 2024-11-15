from tkinter import messagebox

def calculate_fine_and_jail_time(selected_cases, global_jail_time_limit):
    # Calculate total fines and jail time for selected cases
    total_fine = 0
    total_jail_time = 0
    for case_data in selected_cases:
        if 'quantity' in case_data:
            quantity = case_data['quantity']
            fine = case_data['payment'] * quantity
            jail_time = case_data['jail_time'] * quantity if quantity < case_data['threshold'] else case_data['jail_time_limit']
        else:
            fine = case_data['payment']
            jail_time = case_data['jail_time']

        total_fine += fine
        total_jail_time += jail_time

    total_jail_time = min(total_jail_time, global_jail_time_limit)
    return total_fine, total_jail_time

def validate_and_prepare_cases(case_checkboxes, case_entries):
    # Check and prepare selected case information.
    selected_cases = []
    for case_var, case in case_checkboxes:
        if case_var.get():  # If the case is selected
            case_data = {
                'case_name': case['case_name'],
                'payment': case['payment'],
                'jail_time': case['jail_time']
            }

            if case.get("requires_quantity", True):
                quantity_entry = case_entries.get(case['case_name'])
                if quantity_entry:  # Check whether the value is obtained from the entry or not
                    try:
                        quantity = int(quantity_entry.get())
                        case_data['quantity'] = quantity
                        case_data['threshold'] = case['threshold']
                        case_data['jail_time_limit'] = case['jail_time_limit']
                    except ValueError:
                        messagebox.showerror("Error", f"กรุณาระบุจำนวนที่ถูกต้องสำหรับคดี '{case['case_name']}'")
                        return None  # If there is an error in entering the quantity

            selected_cases.append(case_data)

    # Create a list of selected case names
    selected_case_names = [
        f"{case['case_name']} (จำนวน: {case['quantity']})" if 'quantity' in case else case['case_name']
        for case in selected_cases
    ]
    return selected_cases, selected_case_names