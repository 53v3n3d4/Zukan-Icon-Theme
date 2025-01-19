import sublime


def visible_syntaxes_only() -> set:
    """
    Create a list of user ST installed syntaxes, visible only.

    Returns:
    syntaxes_list_visible (set) -- list of user ST installed syntaxes, excluded
    hidden syntaxes.
    """
    syntaxes_list_visible = set()

    all_syntaxes = sublime.list_syntaxes()
    for s in all_syntaxes:
        # When testing without Ruamel, the result of sublime list_syntaxes bring
        # icons syntaxes with hidden false, even though they are all marked as
        # hidden true.
        if not s.hidden and not s.path.startswith(
            'Packages/Zukan Icon Theme/icons_syntaxes/'
        ):
            # print(s.name, s.path, s.hidden)
            # print(os.path.abspath(s.path))
            syntaxes_list_visible.add(s)
    return syntaxes_list_visible


def compare_scopes(zukan_icons_data: list) -> list:
    """
    Compare scopes from user ST installed syntaxes and zukan icon syntaxes.

    Returns:
    list_scopes_to_remove (list) -- scopes list that are present in both, user ST
    installed syntaxes and zukan icon syntaxes.
    """
    list_scopes_to_remove = []

    user_syntaxes_dict = {y.scope: y for y in visible_syntaxes_only()}

    for x in zukan_icons_data:
        if x.get('syntax'):
            for s in x['syntax']:
                if s['scope'] in user_syntaxes_dict:
                    # print(s['scope'])
                    list_scopes_to_remove.append(s)

    return list_scopes_to_remove
