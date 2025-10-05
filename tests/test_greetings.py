
from test_package.greetings import hello_world, hello

def test_hello_world_prints_correct_message(capsys):
    # Call the function
    hello_world()
    
    # Capture stdout
    captured = capsys.readouterr()
    
    # Assert the printed output
    assert captured.out == "hello world from test package!\n"

def test_hello_output(capfd):
    name = "Carles"
    hello(name)
    out, err = capfd.readouterr()
    assert out.strip() == "hello Carles from test package!"
    assert err == ""
    