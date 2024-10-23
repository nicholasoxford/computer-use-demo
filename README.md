# Computer Use Macbook Demo

![Screenshot 2024-10-23 at 7 39 51 AM](https://github.com/user-attachments/assets/f1321098-e650-437c-83bd-5ce8f4cf1c32)


> [!WARNING]
> Computer use is a beta feature. Please be aware that computer use poses unique risks that are distinct from standard API features or chat interfaces. These risks are heightened when using computer use to interact with the internet. To minimize risks, consider taking precautions such as:
>
> 1. Use a dedicated virtual machine or container with minimal privileges to prevent direct system attacks or accidents.
> 2. Avoid giving the model access to sensitive data, such as account login information, to prevent information theft.
> 3. Limit internet access to an allowlist of domains to reduce exposure to malicious content.
> 4. Ask a human to confirm decisions that may result in meaningful real-world consequences as well as any tasks requiring affirmative consent, such as accepting cookies, executing financial transactions, or agreeing to terms of service.
>
> In some circumstances, Claude will follow commands found in content even if it conflicts with the user's instructions. For example, Claude instructions on webpages or contained in images may override instructions or cause Claude to make mistakes. We suggest taking precautions to isolate Claude from sensitive data and actions to avoid risks related to prompt injection.
>
> Finally, please inform end users of relevant risks and obtain their consent prior to enabling computer use in your own products.

> [!CAUTION]
> By using computer-use-mac-demo, you are ignoring the above warnings. Use at your own risk.

This repository helps you get started with controlling your mac using `computer use` on Claude, with reference implementations of:

- Install dependencies and run the python script to start the agent loop
- A computer use agent loop using the Anthropic API to access the updated Claude 3.5 Sonnet model
- Extends Anthropic-defined computer use tools to include additional tools for interacting with your mac
- A streamlit app for interacting with the agent loop

> [!IMPORTANT]
> The Beta API used in this reference implementation is subject to change. Please refer to the [API release notes](https://docs.anthropic.com/en/release-notes/api) for the most up-to-date information.

### Run locally

```bash
ANTHROPIC_API_KEY=your_key_here ./setup.sh # pass your Anthropic API key as an environment variable or set it in browser.
```

Once the python script is running, open your browser to [http://localhost:8080](http://localhost:8080) to access th interface that includes both the agent chat.

Alternative access points:

- Streamlit interface only: [http://localhost:8501](http://localhost:8501)
