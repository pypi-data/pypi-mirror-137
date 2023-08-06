![Proper Forms](header.png)

Proper Forms is a flexible form library to make far easier to create beautiful, semantically rich, syntactically awesome, readily stylable and wonderfully accessible HTML forms in your Python web application.

**Documentation**: https://proper-forms.scaletti.dev


```bash
pip install proper-forms
```

## How Proper Forms is different

- A field isn't tied to a specific HTML tag, so can be presentend in multiple ways. Even the same form can be used in different contexts and have different widgets and styles on each. A set of options as checkboxes, a select multiple, or a comma-separated input? You got it. A date as a calendar or as three selects? No problem.

- Many commonly used built-in validators, and you can also write simple functions to use as custom ones.

- Any field can accept multiple values; as a list or as a comma-separated text.

- All error messages are customizable. The tone of the messages must be able to change or to be translated.

- Incredible easy to integrate with any ORM (object-relational mapper). Why should you need *another* library to do that?


## Just show me how it looks

```python
from proper_forms import Form, Email, Text


class CommentForm(Form):
    email = Email(required=True, check_dns=True)
    message = Text(
    	LongerThan(5, "Please write a longer message"),
    	required=True
    )


def comment():
    form = CommentForm(request.POST)
    if request.method == "POST" and form.validate():
    	data = form.save()
        ...
    return render_template("comment.html", form=form)

```
