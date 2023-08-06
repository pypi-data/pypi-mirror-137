from ipywidgets import Button, Dropdown

def prev_dropdown_next(description, options, on_change):
    def get_prev_next_functions(dropdown):
        def on_prev(b):
            dropdown.value = (dropdown.value - 1) % len(dropdown.options)
        def on_next(b):
            dropdown.value = (dropdown.value + 1) % len(dropdown.options)
        return on_prev, on_next
    dropdown = Dropdown(
        description = description,
        value = 0,
        options = options
    )
    dropdown.observe(on_change, names = "value")
    prev_button = Button(description = "< Prev")
    next_button = Button(description = "Next >")
    on_prev, on_next = get_prev_next_functions(dropdown)
    prev_button.on_click(on_prev)
    next_button.on_click(on_next)
    return prev_button, dropdown, next_button
