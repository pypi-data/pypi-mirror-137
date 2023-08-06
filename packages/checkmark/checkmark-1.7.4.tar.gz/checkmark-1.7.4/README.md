# Checkmark

Checkmark lets you quickly and easily set up a way for you or any other user to submit data to your program through an HTML form. Using a Markdown-like document, you can specify a plethora of form elements.

### Form elements

- [Inlines](#inlines)
    - [Label](#label)
    - [Text & Textarea](#text-textarea)
        - [Text](#text)
        - [Textarea](#textarea)

    - [Checkbox](#checkbox)
    - [Button](#button)
    
- [Lists](#lists)
    - [Radio buttons](#radio-buttons)
    - [Dropdown menu](#dropdown-menu)


## Example

```py
from checkmark import MarkdownForm

document = """
:[Username](username)
>[Username](username "Ex. @user:domain.tld")
:[Password](password)
>[Password](password "Choose something not too simple.")

<!-- A button that calls the `register` API method. -->
@[Register](register)
"""

form = MarkdownForm(
    title='My Markdown Form',
    document=document
)

# Define a function to be called
# when you press the `Register` button.

@form.api_method
def register(data):
    username = data.get('username', "")
    password = data.get('password', "")

    form.update(data, keys=['username', 'password'])

    print(f'Successfully registered as {username}')
    print(f'Your password is {"*" * len(password)}.')

form.start()
```

You can try it out with the example below.

```md
# Account

## Registration

:[Username](username)
>[Ex. @michael:duckduckgo.com](username "@user:domain.tld")<br>
:[Password](password)
>[password123](password "Choose something not too simple.")<br>
:[Email](email)
>[Ex. user@domain.tld](email "So that you can confirm your account.")<br>

[x] [Sign me up to the newsletter](newsletter)

>>[My hobbies are ...](hobbies "What do you like to do during your free time?")

@[Register](register "Register new account.")


## Settings

## layout:
* [IRC](irc)
* [Modern](modern)
* [Message bubbles](bubbles)

## language:
- [Swedish](se)
- [English](en)
- [French](fr)

@[Save settings](save_settings)
```


## Rules

### Inlines

Inline elements can be written anywhere on the line. As long as the pattern is matched, it should create an element in the right place.

#### Link

***This is not a custom element of its own.*** It's a description of how the standard Markdown link format is used within other custom elements.

In any and all definitions, if something looks like a Markdown link, it *is* a Markdown link and should be structured like one. It follows the same rules as regular Markdown and so the title is optional.

The title is always used as the `title` argument for any Checkmark element in which it is specified.

```md
[Text](url "Title.")
```

#### Label

Labels are simply aesthetic and don't affect the functionality of the form.
The URL is only used to define the `for` argument.

```md
:[Super Label](best-label)
```

#### Text & TextArea

`Text` uses one `>` as prefix and `TextArea` uses two.
The text of the link is used as the `placeholder` argument.

##### TextArea
```md
>>[My hobbies are ...](hobbies "What do you like to do during your free time?")
```

##### Text
```md
>[Username](username "Ex. @user:domain.tld")
```

#### Checkbox
```md
[x] [I understand how checkboxes work.](understood)
```

#### Button

Call one of the provided API methods using a button, with the URL as the function name.

```md
@[Log in](log_in)
```

### Lists

A list has a variable name and the possible values for it. The variable name is defined by a preceding heading's Markdown link URL. The URLs of the entries are used for the values. Any empty lines terminate the list, whether between entries or the entries and the heading.

#### Radio Buttons

Radio button entries use `*` as prefix.

```md
## [Message layout](layout):
* [IRC](irc)
* [Modern](modern)
* [Message bubbles](bubbles)
```

#### Dropdown Menu

Dropdown menu entries use `-` as prefix.

```md
## [Language](language):
- [Swedish](se)
- [English](en)
- [French](fr)
```

#### Extensible List (Not yet implemented)

I will be adding lists that allow you to define multiple types of elements per entry and with a `+` button, you will be able to add new multi-element entries into the list.

The future syntax will look a little something like this:

```md
# advanced-dns:
+ ## type:
  - [A Record](a)
  - [CNAME Record](cname)
  - [TXT Record](txt)
+ >[Host](host)
+ >[Port](port)
+ [x] [Backward compatible](backcomp)
```

This list would include a dropdown menu, two text inputs, and a checkbox.
I'll describe it more in detail once I get it implemented.