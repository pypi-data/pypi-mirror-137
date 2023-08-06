# Python Package Boilerplate
Making it easy to create a reusable python package hosted on our internal package manager Nexus.

![Alt_Text](https://source.unsplash.com/8N6z4yXUkwY)

---

## Steps
### 1. Create your python code inside of src > your_package_name > name_me.py
### 2. Update setup.cfg in the project root.
### 3. When you are ready to package your code, [generate your distribution archives](#generating-distribution-archives)
### 4. Upload to a package manager
<ul>

#### 4a. [Nexus - Private Packages](#upload-to-nexus): ACV use.
#### 4b. [PyPi - Public Packages](#upload-to-pypi): For personal projects only.
</ul>

---

## Generating Distribution Archives
1. `python3 -m pip install --upgrade build`
2. `python3 -m build`

This command should output a lot of text and once completed should generate two files in the dist directory:

<ul>
    dist/<br>
        <ul>
        example_package_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl <br>
        example_package_YOUR_USERNAME_HERE-0.0.1.tar.gz
        </ul>
</ul>

---

## Upload To Nexus
Instructions coming soon...

---

## Upload To PyPi
You will need a [registered account](https://pypi.org/account/register/).

1. `python3 -m pip install --upgrade twine`
2. `python3 -m twine upload --repository testpypi dist/*`
3. The terminal will promp you to enter your username and password
