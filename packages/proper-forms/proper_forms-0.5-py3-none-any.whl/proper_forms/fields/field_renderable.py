from uuid import uuid4

from markupsafe import Markup, escape_silent

from ..ftypes import type_boolean
from ..utils import get_html_attrs


__all__ = ("FieldRenderable", "get_html_attrs", "in_")


class FieldRenderable(object):
    def render_attrs(self, **attrs):
        html = get_html_attrs(attrs, show_error=self.error)
        return Markup(html)

    def label(self, text, html="", **attrs):
        text = escape_silent(str(text))
        attrs.setdefault("for", self.name)
        html_attrs = get_html_attrs(attrs, show_error=self.error)
        if html:
            html = html + " "
        return "<label {}>{}{}</label>".format(html_attrs, html, text)

    def as_input(self, *, label=None, value_index=0, **attrs):
        """Renders the field as a `<input type="text">` element, although the type
        can be changed.

        value_index (int):
            If `multiple` is True but the field display only one value,
            this is the index of the value that will be used.
            By default this is 0.
            If the list of values is not long enough, the value used is
            an empty string.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        value = self.get_value(value_index)
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)
        attrs.setdefault("type", self.input_type)
        attrs.setdefault("value", value)
        html_attrs = get_html_attrs(attrs, show_error=self.error)

        html = "<input {}>".format(html_attrs)
        if label:
            kwargs = {"for": attrs.get("id", self.name)}
            html = self.label(label, **kwargs) + "\n" + html
        return Markup(html)

    def as_textarea(self, *, label=None, value_index=0, **attrs):
        """Renders the field as a `<textarea>` tag.

        value_index (int):
            If `multiple` is True but the field display only one value,
            this is the index of the value that will be used.
            By default this is 0.
            If the list of values is not long enough, the value used is
            an empty string.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)

        value = attrs.pop("value", None) or self.get_value(value_index)
        html_attrs = get_html_attrs(attrs, show_error=self.error)
        html = "<textarea {}>{}</textarea>".format(html_attrs, value)
        if label:
            kwargs = {"for": attrs.get("id", self.name)}
            html = self.label(label, **kwargs) + "\n" + html
        return Markup(html)

    def as_richtext(self, *, label=None, value_index=0, **attrs):
        """Renders the field as a `<trix-editor>` tag with a matching
        hidden input file.

        Thi sonly render the tags, you must include the `trix.css` and `trix.js` files
        in the <head> of your page to make it a working rich-text editor
        (See https://github.com/basecamp/trix#getting-started).

        value_index (int):
            If `multiple` is True but the field display only one value,
            this is the index of the value that will be used.
            By default this is 0.
            If the list of values is not long enough, the value used is
            an empty string.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        name = attrs.pop("name", self.name)
        value = attrs.pop("value", None) or self.get_value(value_index)
        input_id = attrs.pop("id", str(uuid4()))

        attrs["input"] = input_id
        attrs.setdefault("required", self.required)
        attrs.setdefault("classes", "trix-content")
        if label:
            attrs["aria-labelledby"] = f"label-{input_id}"

        html_attrs = get_html_attrs(attrs, show_error=self.error)
        html = "\n".join([
            f'<input id="{input_id}" name="{name}" value="{value}" type="hidden">',
            f"<trix-editor {html_attrs}></trix-editor>",
        ])
        if label:
            kw = {"id": f"label-{input_id}", "for": False}
            html = self.label(label, **kw) + "\n" + html
        return Markup(html)

    def as_checkbox(self, *, label=None, **attrs):
        """Renders the field as a `<input type="checkbox">` tag.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs["type"] = "checkbox"
        attrs.setdefault("required", self.required)

        value = attrs.get("value")
        if value is not None:
            attrs.setdefault("checked", in_(value, self.values))
        else:
            attrs.setdefault("checked", type_boolean(self.value))
        html_attrs = get_html_attrs(attrs, show_error=self.error)

        html = "<input {}>".format(html_attrs)
        if label:
            kwargs = {"for": None, "classes": attrs.get("classes", "checkbox")}
            html = self.label(label, html=html, **kwargs)

        return Markup(html)

    def as_radio(self, *, label=None, **attrs):
        """Renders the field as a `<input type="radio">` tag.

        value_index (int):
            If `multiple` is True but the field display only one value,
            this is the index of the value that will be used.
            By default this is 0.
            If the list of values is not long enough, the value used is
            an empty string.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs["type"] = "radio"
        attrs.setdefault("required", self.required)

        value = attrs.get("value")
        if value is not None:
            attrs.setdefault("checked", in_(value, self.values))
        else:
            attrs.setdefault("checked", type_boolean(self.value))
        html_attrs = get_html_attrs(attrs, show_error=self.error)

        html = "<input {}>".format(html_attrs)
        if label:
            kwargs = {"for": None, "classes": attrs.get("classes", "radio")}
            html = self.label(label, html=html, **kwargs)

        return Markup(html)

    def as_select_tag(self, *, label=None, **attrs):
        """Renders *just* the opening `<select>` tag for a field, not any options
        nor the closing "</select>".

        This is intended to be used with `<option>` tags writted by hand or genereated
        by other means.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)
        attrs.setdefault("multiple", self.multiple)
        html_attrs = get_html_attrs(attrs, show_error=self.error)

        html = "<select {}>".format(html_attrs)
        if label:
            kwargs = {"for": attrs.get("id", self.name)}
            html = self.label(label, **kwargs) + "\n" + html

        return Markup(html)

    def as_select(self, items, *, label=None, **attrs):
        """Renders the field as a `<select>` tag.

        items (list):
            ...

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """

        html = [str(self.as_select_tag(label=label, **attrs))]

        for item in items:
            label, value = item[:2]
            if isinstance(value, (list, tuple)):
                tags = self.render_optgroup(label, value)
            else:
                opattrs = item[2] if len(item) > 2 else {}
                tags = self.render_option(label, value, **opattrs)
            html.append(str(tags))

        html.append("</select>")
        return Markup("\n".join(html))

    def render_optgroup(self, label, items, **attrs):
        """Renders an <optgroup> tag with <options>.

        label (str):
            ...

        items (list):
            ...

        values (any|list|None):
            A value or a list of "selected" values.

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs["label"] = escape_silent(str(label))
        html_attrs = get_html_attrs(attrs, show_error=self.error)
        html = ["<optgroup {}>".format(html_attrs)]

        for item in items:
            oplabel, opvalue = item[:2]
            opattrs = item[2] if len(item) > 2 else {}
            tag = self.render_option(oplabel, opvalue, **opattrs)
            html.append(str(tag))

        html.append("</optgroup>")
        return Markup("\n".join(html))

    def render_option(self, label, value=None, **attrs):
        """Renders an <option> tag

        label:
            Text of the option

        value:
            Value for the option (sames as the label by default).

        **attrs:
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        values = self.values or []
        value = label if value is None else value
        attrs.setdefault("value", value)
        attrs["selected"] = in_(value, values)
        label = escape_silent(str(label))
        html_attrs = get_html_attrs(attrs, show_error=self.error)
        tag = "<option {}>{}</option>".format(html_attrs, label)
        return Markup(tag)

    def render_error(self, tag="div", **attrs):
        if not self.error:
            return ""

        attrs.setdefault("classes", "error")
        return Markup(
            "<{tag} {attrs}>{error}</{tag}>".format(
                tag=tag,
                attrs=get_html_attrs(attrs, show_error=False),
                error=self.error,
            )
        )


def in_(value, values):
    """Test if the value is in a list of values, or if the value as string is, or
    if the value is one of the values as strings.
    """
    ext_values = values + [str(val) for val in values]
    return value in ext_values or str(value) in ext_values
