from flask import Flask, request, render_template_string, redirect, url_for
import random

app = Flask(__name__)

# Load character names
with open("static/characters.txt") as f:
    characters = f.read().split(', ')

# Utilities
def make_html(title, body):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <link href="/static/styles.css" rel="stylesheet">
        <title>{title}</title>
    </head>
    <body>{body}</body>
    </html>
    """
    return html


def make_form(action_url, question, radio_options, input_name="choices", default_value=None):
    html = f'<form action="{action_url}" method="GET">{question}<br>'
    for option in radio_options:
        checked = ''
        if default_value and option == default_value:
            checked = ' checked'
        html += f'<div><input type="radio" name="{input_name}" value="{option}"{checked}>{option}</div>'
    html += '<input type="submit" value="Next"></form>'
    return html

def make_text_input_form(action_url, question, input_name="name", default_value=""):
    html = f'''
    <form action="{action_url}" method="GET">
        {question}<br>
        <input type="text" name="{input_name}" value="{default_value}"><br>
        <input type="submit" value="Submit">
    </form>
    '''
    return html

def make_friend_form(question, options):
    return make_form('/game', question, options, input_name="friends")

def make_house_form(question, options):
    return make_form('/game', question, options, input_name="house")

def make_password_form(question, default_password="Mugwart"):
    html = f'''
    <form action="/game" method="GET">
        {question}<br>
        <input type="text" name="password" value="{default_password}"><br>
        <input type="submit" value="Submit">
    </form>
    '''
    return html

# Routes
# Continued from previous code

@app.route('/')
def index():
    # Starting page: ask for name
    body = '<h1>Welcome to the world of Witchcraft and Wizardry!</h1>'
    body += make_text_input_form('/game', 'What is your name?', default_value='Dolores Umbridge')
    return make_html('Begin', body)


@app.route('/game')
def game():
    # Grab all possible query parameters
    name = request.args.get('name', '')
    choice = request.args.get('choices', '')
    friend = request.args.get('friends', '')
    house = request.args.get('house', '')
    password = request.args.get('password', '')

    # PAGE0 to PAGE1
    if name:
        # PAGE1
        question1 = "It is 8:00 AM in the morning, and your alarm goes off. <br> Do you:"
        options1 = ['Snooze, sleep for 5 more minutes', 'Get up and head to the train station!']

        body = f'<h1>Hello {name}</h1>'
        body += make_form('/game', question1, options1)
        return make_html('Mugwarts Magical School', body)

    # PAGE2
    if choice == 'Snooze, sleep for 5 more minutes':
        question2 = "Oh no! You woke up too late, and missed your train! Unfortunately, there's only one train time every year. Or, you think of other ways to get to school. <br> Do you:"
        options2 = ["Take your parents' flying car", 'Send an owl to the Principal to get someone to come pick you up']

        body = '<h1>You Snooze, you Lose!</h1>'
        body += make_form('/game', question2, options2)
        return make_html('You Snooze, you Lose!', body)

    # PAGE3 or PAGE4
    if choice == "Take your parents' flying car":
        # PAGE3 - Expelled
        body = ('<h1>Wow…Rebel</h1>\n'
                '<p>You took the magic car… but it broke down and you landed in the forbidden forest. '
                'After you get out, Ms Mcgonagall catches you and… YOU WERE EXPELLED!</p>'
                'The End...<br><a href="/">Try Again?</a>')
        return make_html('Wow…Rebel', body)
    
    if friend == '':
        chosen_friend = random.choice(characters)
        return redirect(url_for('game', friends=chosen_friend))

    if choice == 'Send an owl to the Principal to get someone to come pick you up' or choice == 'Get up and head to the train station!':
        # PAGE4 - Hagrid arrives
        body = ('<h1>Meet Hagrid!</h1>\n'
                '<p>Hagrid is sent to pick you up on his motorcycle. You get to school quickly in time for the big feast '
                'and to witness the new coming wizards and witches!</p>'
                f'<a href="/game?friends={friend}">Time for the Feast!</a>')
        return make_html('Meet Hagrid!', body)

    # PAGE5

    

    if friend:
        # Choose a friend randomly (you had random.sample in CGI)
        body = ('<h1>On the Train</h1>\n'
                '<p>On the train, your BFF is nowhere to be seen. You walk through, and all the compartments are filled, except for 1.</p>'
                f"<p> You're forced to sit with {friend}. They quickly become your new friend."
                '<p>You talk for the remainder of the commute to Mugwarts Magical High School, and arrive at a big feast waiting for you.</p>'
                f'<a href="/game?friends={friend}&choices=next6">Time for the Feast!</a>')
        return make_html('On the Train', body)

    # PAGE6
    if friend and choice == "next6":
        question6 = "What house are you part of?(Hufflepuff doesn't exist for a reason.)"
        options6 = ['Gryffindor', 'Slytherin', 'Ravenclaw']
        body = '<h1>Time for a feast!</h1>'
        body += make_house_form(question6, options6)
        return make_html('Time for a feast!', body)

    # PAGE7 and onward: House chosen
    if house in ['Gryffindor', 'Slytherin', 'Ravenclaw']:
        body = (f'<h1>Welcome to {house}!</h1>'
                f"<p>After dinner, you go to your house's dorm.</p>"
                "<br>Your password is DobbylovesMugwarts, be sure to remember this!<br>"
                "You've met your roommate, his name is Harry Potter, he's a pretty average guy.<br>"
                '<p>Zzzzzzz…</p><br>'
                "<a href='/game?choices=next'>Next</a>")
        return make_html(f'Welcome to {house}!', body)

    # PAGE 8 and forward - example for choice 'next'
    if choice == 'next':
        add = ("<h1>A Few Weeks Later...</h1>\n<p>You, your roommate, and your friend are now a trio. Strange things have happened in school: <br>"
               '1. People have been found petrified throughout the school.<br>'
               "2. There's bloody writing on the walls where the victims are found.</p>"
               "<a href='/game?choices=next1'>Next</a>")
        return make_html('A Few Weeks Later', add)

    # PAGE 9
    if choice == 'next1':
        question8 = 'Do you:'
        options8 = ["Analyze the writing on the wall", 'Wait for the victim to wake up', "Search the victim's dorm"]
        body = ("<h1>Someone new has just been found petrified.</h1>\n"
                "<p>Your trio wants to find out what's been happening.</p>")
        body += make_form('/game', question8, options8)
        return make_html('Someone new has just been found petrified', body)

    # PAGE9
    if choice == 'Analyze the writing on the wall':
        question9 = 'What do you do?'
        options9 = ['Ask Hagrid about the Chamber of Secrets', 'Ask Professor McGonagall about the Chamber of Secrets']
        body = ('<h1>The Writing on the Wall</h1>'
                '<p>The writing says: <br> “The Chamber of Secrets has been opened. Enemy of the heir beware” </p>')
        body += make_form('/game', question9, options9)
        return make_html('The Writing on the Wall', body)

    # PAGE10
    if choice == 'Ask Hagrid about the Chamber of Secrets':
        question10 = 'Where do you go to investigate?'
        options10 = ['The 3rd floor library', 'The Hufflepuff common room', 'The bathroom next to the library']
        body = ("<h1>Hagrid can't Keep a Secret…</h1>"
                '<p>Hagrid tells you the history of the Chamber of Secrets, and how a muggle was killed when he was a student at Mugwarts. '
                "He tells you how to open the Chamber of Secrets, but he doesn't know where it is. He gives you a clue, telling you where the muggle was killed: "
                '“She was a hufflepuff, and she was found in the 3rd floor library.”</p>')
        body += make_form('/game', question10, options10)
        return make_html("Hagrid can't Keep a Secret…", body)

    # PAGE11
    if choice == 'The 3rd floor library':
        question11 = 'Which one should you investigate?'
        options11 = ['The one with a serpent on the spine','The one with a dragon on the spine', 'The one with a bird on the spine']
        body = ("<h1>Where's the entrance?</h1>"
                "<p>You go to the library, and there's nothing suspicious. Your roommate starts scanning all of the books. There are three that stand out.</p>")
        body += make_form('/game', question11, options11)
        return make_html("Where's the entrance?", body)

    # PAGE12
    if choice in ['The one with a serpent on the spine', 'The one with a bird on the spine']:
        body = ('<h1>Error...</h1>'
                '<p>There was nothing useful in the book.</p>'
                '<br><a href="/game?choices=The+3rd+floor+library">Try Another Book</a>')
        return make_html('Error...', body)

    # PAGE13
    if choice == 'The one with a dragon on the spine':
        question13o = 'Who do you choose to come with you?'
        options13o = ['Harry Potter', 'Your friend']
        body = ('<h1>Open Sesame</h1>'
                '<p>You pulled on the book, and a staircase emerged! You and your friends follow it to a dark chamber. <br>Lumos!  <br>There are a hundred pixies carrying keys. '
                'Only one opens the door on the other side of the chamber. However, there are only two broomsticks for you to ride to find the key. </p>')
        body += make_form('/game', question13o, options13o)
        return make_html('Open Sesame', body)

    # PAGE13 part 2: after choosing who comes along
    if choice in ['Harry Potter', 'Your friend']:
        nochoose = 'Harry Potter' if choice == 'Your friend' else 'Your friend'
        question13t = 'Which weapon do you choose to use?'
        options13t = ['The Gryffindor Sword', 'A stone', 'Your Wand']
        body = (f'<h1>Open Sesame</h1>'
                f'<p>{nochoose} stays behind, and goes to get more help. You and {choice} continue on. '
                f"You and {choice} go into a larger chamber. Something eerie is happening… You see a figure lying on the ground, and you go closer. It's your long lost BFF!!! "
                f'Now, you must save your BFF by slaying the Dragon that is emerging from his slumber. </p>')
        body += make_form('/game', question13t, options13t)
        return make_html('Open Sesame', body)

    # PAGE14
    if choice == 'The Gryffindor Sword':
        body = ("<h1>You're Delusional... </h1>"
                "<p>Umm... Sorry but there is no Gryffindor Sword. The Dragon eats you and all your friends.</p>"
                'The End...<br><a href="/">Try Again?</a>')
        return make_html("You're Delusional...", body)

    # PAGE15
    if choice == 'A stone':
        body = ('<h1>Rock beats Scissors</h1>'
                '<p>Yay! You killed the dragon by stabbing its heart with the small but sharp pebble. You saved everyone, including your BFF.</p>'
                'The End...<br><a href="/">Try Again?</a>')
        return make_html('Rock beats Scissors', body)

    # PAGE16
    if choice == 'Your Wand':
        question16 = 'Which spell would you like to use? '
        options16 = ['Incendio!', 'Petrificus Totalus!']
        body = '<h1>Finally using some magic…</h1>'
        body += make_form('/game', question16, options16)
        return make_html('Finally using some magic...', body)

    # PAGE17
    if choice == 'Incendio!':
        body = ('<h1>Stop. Drop. and Roll</h1>'
                "<p>Incendio lit the dragon on fire, but it's fireproof, and got super pissed. It instead lights your friend on fire… They die… "
                'Your other friend who went to get help arrives just in time for you to save yourself and your BFF. You saved the school, but at what cost? </p>'
                'The End...<br><a href="/">Try Again?</a>')
        return make_html('Stop. Drop. and Roll.', body)

    # PAGE18
    if choice == 'Petrificus Totalus!':
        body = ('<h1>Clever, feed them their own Poison</h1>'
                '<p>You managed to petrify the beast! (How ironic!). Your friend who went to get help arrived to rescue everyone, '
                'and the teachers dealt with the dragon. You saved the school!</p>'
                'The End...<br><a href="/">Try Again?</a>')
        return make_html('Clever, feed them their own Poison', body)

    # PAGE19
    if choice == 'The bathroom next to the library':
        body = ('<h1>Squeaky Clean</h1>'
                "<p>There's nothing in the bathroom… </p>"
                '<br><a href="/game?choices=Ask+Hagrid+about+the+Chamber+of+Secrets">Go Back</a>')
        return make_html('Squeaky Clean', body)

    # PAGE20
    if choice == 'The Hufflepuff common room':
        body = ('<h1>No Trespassing!</h1>'
                "<p>You can't get into the Hufflepuff common room, because you're not a Hufflepuff! </p>"
                '<br><a href="/game?choices=Ask+Hagrid+about+the+Chamber+of+Secrets">Go Back</a>')
        return make_html('No Trespassing!', body)

    # PAGE21
    if choice == 'Ask Professor McGonagall about the Chamber of Secrets':
        body = ("<h1>Isn't it Past Curfew!? </h1>"
                '<p>Professor McGonagall does not want students to be snooping around. She is no help, so you find another solution.</p>'
                'The End...<br><a href="/game?choices=next1">Find Another Solution</a>')
        return make_html("Isn't it Past Curfew!?", body)

    # PAGE22 (password input)
    if choice == "Search the victim's dorm":
        question22 = 'What is the password to your dorm?(Capitalization does matter)'
        body = ('<h1>Password Please</h1>'
                '<p>The victim belongs to your dorm</p>')
        body += make_password_form(question22, default_value='Mugwart')
        body += '<br><a href="/game?choices=Forgot+Password">Forgot Password</a>'
        return make_html('Password Please', body)

    # PAGE23 (forgot password)
    if choice == 'Forgot Password':
        body = ('<h1>You Forgot the Password!</h1>'
                '<p>You were stopped in your search, and could not find our what was happening. Mugwarts Magical High School was eaten by a dragon.</p>'
                'The End...<br><a href="/">Try Again?</a>')
        return make_html('You Forgot the Password!', body)

    # PAGE24 (correct password)
    if password == 'DobbylovesMugwarts':
        question24 = 'Do you:'
        options24 = ['Ask Hagrid about the Chamber of Secrets', 'Go to the location', "Give up because you don't want to die"]
        body = ("<h1>You're in!</h1>"
                '<p>You, Harry Potter, and your friend search through the dorm.</p>'
                "<p> Harry finds the victim's diary. The diary details everything that the victim was doing before they were found petrified, "
                "including a story about the Chamber of Secrets. There is a crazy dragon that is waiting to break out. "
                "He also performs a spell to find a note with a location and a drawing of a dragon on it  </p>")
        body += make_form('/game', question24, options24)
        return make_html("You're in!", body)

    # PAGE25 (wrong password)
    if password and password != 'DobbylovesMugwarts':
        body = ('<h1>No one remembers the password!</h1>'
                '<p>Oh no… you couldn\'t get into your dorm, so you never figured out what happened. '
                'A large dragon shot out of the girls bathroom toilet and ended up killing everyone… MUGWARTS SCHOOL OF MAGIC IS DEAD…</p>'
                'The End...<br><a href="/">Try Again?</a>')
        return make_html('No one remembers the password!', body)

    # PAGE26 (Waited too long)
    if choice == 'Wait for the victim to wake up':
        body = ('<h1>You Took too Long…</h1>'
                '<p>The Mandrakes, which are needed to cure the petrified, took too long to grow. '
                'A large dragon ended up getting loose in the school and killed everyone… MUGWARTS SCHOOL OF MAGIC IS DEAD… </p>'
                '<br><a href="/">Try Again?</a>')
        return make_html('You Took too Long…', body)

    # PAGE27 (give up)
    if choice == "Give up because you don't want to die":
        body = ('<h1>What a wimp!</h1>'
                '<p>You gave up because you were too scared...you couldn\'t uncover the truth.</p>'
                '<br><a href="/">Try Again?</a>')
        return make_html('What a wimp!', body)

    # Default fallback: restart page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
