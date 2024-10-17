def input_error(func): # Функція для обробки помилок вводу
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            return str(e)
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
    return wrapper
