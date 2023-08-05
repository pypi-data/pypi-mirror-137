from distutils.core import setup, Extension

def main():
    setup(
          name="forbidden_keys",
          version="1.0.0",
          description="Module for checking forbidden keys",
          author="Nagy Zoltán",
          author_email="zolika3400@gmail.com",
          ext_modules=[Extension('forbidden_keys', ['forbidden_keys.c'])]
          )

if __name__ == "__main__":
    main()
