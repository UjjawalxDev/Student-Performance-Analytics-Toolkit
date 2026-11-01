# Student Performance Analytics Toolkit

SUBJECTS=('Python','Maths','DBMS')


# Calculate total marks
def calculate_total(marks):
    return sum(marks)


# Calculate average marks

def calculate_average(marks):
    if len(marks)==0:
        return 0
    return sum(marks)/len(marks)

# Calculate grade

def get_grade(average):
    if average >=75:
        return "Distinction"
    elif average>=60:
        return "First Division"
    else:
        return "Fail"
    

# Validate and create student record
# Returns (True, record) on success or (False, error message) on failure

def add_student(student_id, name, marks):
    if student_id=="":
        return False, "Student ID can't be empty."
    if name=="":
        return False, "Nmae can't be empty."
    if len(marks)!=len(SUBJECTS):
        return False, "Exactly"+str(len(SUBJECTS))+"maeks are required."
    for marks in marks:
        if marks < 0 or marks >100:
            return False, "marksa must be beetween 0 and 100."
        return True, {"name":name,"marks":marks}

# Build student report

def build_report(student):
    marks=student["marks"]
    average=calculate_average(marks)

    return{
        "name": student["name"],
        "marks": marks,
        "total":calculate_total(marks),
        "average":average,
        "grade": get_grade(average),
    }

# Find high-performing students (filter + map with lambda)

def get_top_students(records):
    top=filter(
        lambda item: calculate_average(item[1]["marks"]) >=75,
        records.item()
    )
    return list(map(lambda item:item[1]["marks"],top))

# Average of any number of marks using *args

def marks_average(*marks):
    if len(marks)==0:
        return 0
    return sum(marks)/len(marks)

# Class summary with default arguments
def class_summary(records, title="Class Report", passing_mark=40):
    averages = []
    for student in records.values():
        averages.append(calculate_average(student["marks"]))

    print("\n====", title, "====")
    print("Total students:", len(records))

    if averages:
        print("Class average:", format(sum(averages) / len(averages), ".2f"))

    passed = 0
    for average in averages:
        if average >= passing_mark:
            passed += 1

    print("Students meeting passing mark (" + str(passing_mark) + "):", passed)


# Named summary options using **kwargs
def describe_options(**options):
    parts = []
    for key, value in options.items():
        parts.append(key + "=" + str(value))
    return ", ".join(parts)


# Recursion
def recursive_sum(n):
    if n <= 0:
        return 0
    return n + recursive_sum(n - 1)


# Local vs global scope
counter = 0


def scope_example():
    message = "This is a local variable"     # exists only inside this function
    print(message)


def global_example():
    global counter                             # used only to show its effect
    counter = counter + 1  


# Safe integer input      
def read_int(message, low=None, high=None):
    while True:
        try:
            value = int(input(message))
        except ValueError:
            print("Please enter a whole number.")
            continue

        if low is not None and value < low:
            print("Value must be at least", low)
        elif high is not None and value > high:
            print("Value must be at most", high)
        else:
            return value



#take record from the user and return them as a dictionary

def collect_students():
    students = {}
    count = read_int("How many students? ", low=1)

    for i in range(count):
        print("\nEnter details for student", i + 1)

        student_id = input("Student ID: ").strip()
        while student_id in students:
            print("This ID already exists.")
            student_id = input("Enter another ID: ").strip()

        name = input("Student name: ").strip()

        marks = []
        for subject in SUBJECTS:
            marks.append(read_int(subject + " marks: ", low=0, high=100))

        ok, result = add_student(student_id, name, marks)   # positional arguments
        if ok:
            students[student_id] = result
        else:
            print("Invalid record:", result)

    return students



#print the every recod for every student
def display_reports(students):
    print("\n====== STUDENT PERFORMANCE REPORT ======")

    for student_id, student in students.items():
        report = build_report(student)
        print(student_id, "|", report["name"], "| Marks:", report["marks"])
        print("Total:", report["total"],
              "| Average:", format(report["average"], ".2f"),
              "| Grade:", report["grade"])


# Show the recursion tests
def run_recursion_tests():
    print("\n===== RECURSION TEST =====")
    for n in (3, 5, 7):
        print("Sum from 1 to", str(n) + ":", recursive_sum(n))


# Show the scope examples
def run_scope_demo():
    print("\n===== SCOPE EXAMPLE =====")
    scope_example()
    global_example()
    print("Global counter after calling global_example():", counter)


def main():
    print("===== STUDENT PERFORMANCE ANALYTICS =====")

    students = collect_students()
    display_reports(students)

    print("\nHigh performers (average >= 75):", get_top_students(students))

    names = list(map(lambda student: student["name"], students.values()))
    print("All student names:", names)

    print("\nAverage of supplied marks:", marks_average(80, 70, 90))

    # Keyword arguments
    class_summary(students, title="Class Performance Report", passing_mark=50)
    # Default arguments
    class_summary(students)

    print("\nSummary options:", describe_options(title="Class Report", passing_mark=40))

    run_recursion_tests()
    run_scope_demo()


if __name__ == "__main__":
    main()