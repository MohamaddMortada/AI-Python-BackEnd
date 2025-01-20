def calculate_accuracy(angles_data):
    total = len(angles_data)
    correct = sum(1 for value in angles_data.values() if value == True)
    incorrect = total - correct
    
    correct_percentage = (correct / total) * 100
    incorrect_percentage = (incorrect / total) * 100
    
    return correct_percentage, incorrect_percentage