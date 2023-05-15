# BeeDeeBeeDee

Inspired by https://kadekillary.work/posts/1000x-eng/ I wanted to do this in 
Python (because I don't like shell scripting if I can help it).

Put a toml file with this content at `~/.openai-config.toml`
    ```
    [api]
    token = "YOUR_OPEN_AI_TOKEN"
    url = "https://api.openai.com/v1"
    ```

Install via pipx like `pipx install git+https://github.com/ryangadams/beedeebeedee.git`

Then run it like `hal "Your prompt here"` or `dali "YOUR IMAGE PROMPT HERE"`

