"""Main loop file."""

from ft_parser import tokenize, parse
from execution import execute

if __name__ == "__main__":
    while True:
        try:
            val = input("==> : ").strip().replace(" ", '')
            if val == "":
                continue
            try:
                tokens = tokenize(val)
                parsed = parse(tokens)
                result = execute(parsed["type"], parsed["tokens"], val)
                if result is not None:
                    print(result)
            except SyntaxError as e:
                print(f"Error - Invalid syntax : {e}")
            except ValueError as e:
                print(f"Error - Invalid value : {e}")
            except AttributeError as e:
                print(f"Error - Unsupporte operation : {e}")
            except IndexError as e:
                print(f"Error - Unknown variable or function {e}")
            except ZeroDivisionError:
                print("Error - Cannot divide by 0 !")
        except EOFError:
            print("\nExiting ...")
            break
        except KeyboardInterrupt:
            print("\nExiting ...")
            break
        except ValueError as e:
            print(e)
