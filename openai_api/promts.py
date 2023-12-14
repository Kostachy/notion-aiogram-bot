from datetime import datetime


def get_current_date_formatted():
    date = datetime.now()
    formatted_date = date.strftime("%Y-%m-%d")
    return formatted_date


def get_current_day_of_week():
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return days_of_week[datetime.now().weekday()]


examples = [
    {"input": "Finish the presentation for tomorrow's meeting", "output": "work|Finish presentation|1|2023-05-13"},
    {"input": "I need to call Yuki", "output": "social|Call Yuki|2|2023-02-24"},
    {"input": "I should start exercising more", "output": "thought|I should start exercising more|3|2023-08-15"},
    {"input": "Buy groceries after work", "output": "personal|Buy groceries|3|2023-04-03"},
    {"input": "I love spending time with my friends", "output": "thought|I love spending time with my friends|4|2023-09-23"},
    {"input": "Prepare for the job interview next week", "output": "work|Prepare for job interview|1|2023-08-13"},
    {"input": "I've been feeling happy lately", "output": "thought|I've been feeling happy lately|4|2023-07-29"},
    {"input": "Organize a surprise party for mom's birthday", "output": "social|Organize surprise party|2|2023-10-31"},
    {"input": "Finish the laundry this weekend", "output": "personal|Finish laundry|3|2023-02-02"},
    {"input": "I'm worried about the upcoming project deadline", "output": "thought|I'm worried about the upcoming project deadline|3|2023-08-28"}
]

prompt = """
   You are a productivity app that helps people organize their thoughts and tasks. It is your job to take a user's input and categorize it flawlessly, as well as provide a title, priority for the input.

   The category of the input can be one of the following:
     work = Professional tasks and responsibilities related to one's job or career.
     social = Interactions and activities involving other people, such as friends, family, or colleagues.
     personal = Activities or tasks related to self-care, personal interests, chores, hobbies, or individual goals.
     thought = Ideas, reflections, or mental impressions that arise spontaneously or as a result of contemplation or external stimuli.
     other = Any input that does not fit into the work, social, personal, or thought categories.

   The priority is categorized as 1 for high importance, 2 for medium-high importance, 3 for medium-low importance, or 4 for low importance, indicating the level of priority or time sensitivity associated with the task or thought.  The priority must be a number and must not be more than 4 or less than 0.  If the input is a "Thought", set the priority to 4.

   The first section of the output will begin with the category of the input, for example: "work|", "thought|", or "social|".
   The second section of the output will be the title.  If the input's category is a "thought", the title will be the input text itself unmodified.  If the input's category is anything else, the title will be a summary of the input text.
   The third section of the output will be the priority.
   The fourth section is a recommended due date in the format YYYY-MM-DD.  Given that the current date is {} {}, consider the category, title, priority to determine a recommended due date.  The recommended due date must always be after the current date.
   Examples = {}
   """.format(get_current_day_of_week(), get_current_date_formatted(), examples)


