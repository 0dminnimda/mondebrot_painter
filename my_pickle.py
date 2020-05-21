import os
import pickle


def dump(name, value, end=".pickle"):
    full_name = check_name(name, end)

    create(name)

    with open(full_name, "wb") as file:
        pickle.dump(value, file)

    return value


def create(name, end=".pickle", only=None):
    full_name = check_name(name, end)

    # existing test
    try:
        open(full_name, "xb").close()
    except Exception: pass

    # filling test
    if not file_size(name) > 0:
        with open(full_name, "wb") as file:
            # create main array
            if only is None:
                pickle.dump([], file)


def load(name, end=".pickle"):
    full_name = check_name(name, end)

    with open(full_name, 'rb') as file:
        return pickle.load(file)


def check_len(name, end=".pickle"):
    return len(load(name, end))


def file_size(name, end=".pickle"):
    full_name = check_name(name, end)

    return os.path.getsize(full_name)


def check_name(name, end):
    if name.starswith(end):
        return name
    else:
        return name + end
