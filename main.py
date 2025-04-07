"""Main loop file."""
from Parser import tokenize, parse
from execution import execute

if __name__ == "__main__":
    while True:
        try:
            val = input("==> : ")
            if val.strip().replace(" ", '') == "":
                continue
            try:
                tokens = tokenize(val)
                parsed = parse(tokens)
                execute(parsed["type"], parsed["tokens"], val)
            except SyntaxError as e:
                print(f"Error - Invalid syntax : {e}")
            except ValueError as e:
                print(f"Error - Invalid value : {e}")
            except AttributeError as e:
                print(f"Error - Unsupporte operation : {e}")
            except IndexError as e:
                print(f"Error - Unknown variable or function {e}")
        except EOFError:
            print("\nExiting ...")
            break
        except KeyboardInterrupt:
            print("\nExiting ...")
            break
        except ValueError as e:
            print(e)