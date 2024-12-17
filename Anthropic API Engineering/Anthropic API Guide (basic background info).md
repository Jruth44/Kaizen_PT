## Getting started

### Accessing the API

The API is made available via our web [Console](https://console.anthropic.com/). You can use the [Workbench](https://console.anthropic.com/workbench/3b57d80a-99f2-4760-8316-d3bb14fbfb1e) to try out the API in the browser and then generate API keys in [Account Settings](https://console.anthropic.com/account/keys). Use [workspaces](https://console.anthropic.com/settings/workspaces) to segment your API keys and [control spend](https://docs.anthropic.com/en/api/rate-limits) by use case. The API key for our project is = 

### Authentication

All requests to the Anthropic API must include an `x-api-key` header with your API key. If you are using the Client SDKs, you will set the API when constructing a client, and then the SDK will send the header on your behalf with every request. If integrating directly with the API, you’ll need to send this header yourself.

### Content types

The Anthropic API always accepts JSON in request bodies and returns JSON in response bodies. You will need to send the `content-type: application/json` header in requests. If you are using the Client SDKs, this will be taken care of automatically.

### Examples

```Python
pip install anthropic

import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my_api_key",
)
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content)
```
## Versions 
When making API requests, you must send an `anthropic-version` request header. For example, `anthropic-version: 2023-06-01`. If you are using our [client libraries](https://docs.anthropic.com/en/api/client-libraries), this is handled for you automatically.

For any given API version, we will preserve:

- Existing input parameters
- Existing output parameters

However, we may do the following:

- Add additional optional inputs
- Add additional values to the output
- Change conditions for specific error types
- Add new variants to enum-like output values (for example, streaming event types)

Generally, if you are using the API as documented in this reference, we will not break your usage.

### Version history

We always recommend using the latest API version whenever possible. Previous versions are considered deprecated and may be unavailable for new users.

- `2023-06-01`
    - New format for [streaming](https://docs.anthropic.com/en/api/streaming) server-sent events (SSE):
        - Completions are incremental. For example, `" Hello"`, `" my"`, `" name"`, `" is"`, `" Claude."` instead of `" Hello"`, `" Hello my"`, `" Hello my name"`, `" Hello my name is"`, `" Hello my name is Claude."`.
        - All events are [named events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#named%5Fevents), rather than [data-only events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#data-only%5Fmessages).
        - Removed unnecessary `data: [DONE]` event.
    - Removed legacy `exception` and `truncated` values in responses.
- `2023-01-01`: Initial release.
## Errors 
### HTTP errors

Our API follows a predictable HTTP error code format:

- 400 - `invalid_request_error`: There was an issue with the format or content of your request. We may also use this error type for other 4XX status codes not listed below.
- 401 - `authentication_error`: There’s an issue with your API key.
- 403 - `permission_error`: Your API key does not have permission to use the specified resource.
- 404 - `not_found_error`: The requested resource was not found.
- 413 - `request_too_large`: Request exceeds the maximum allowed number of bytes.
- 429 - `rate_limit_error`: Your account has hit a rate limit.
- 500 - `api_error`: An unexpected error has occurred internal to Anthropic’s systems.
- 529 - `overloaded_error`: Anthropic’s API is temporarily overloaded.

When receiving a [streaming](https://docs.anthropic.com/en/api/streaming) response via SSE, it’s possible that an error can occur after returning a 200 response, in which case error handling wouldn’t follow these standard mechanisms.

### Error shapes

Errors are always returned as JSON, with a top-level `error` object that always includes a `type` and `message` value. For example:

JSON

```JSON
{
  "type": "error",
  "error": {
    "type": "not_found_error",
    "message": "The requested resource could not be found."
  }
}
```

In accordance with our [versioning](https://docs.anthropic.com/en/api/versioning) policy, we may expand the values within these objects, and it is possible that the `type` values will grow over time.

### Request id

Every API response includes a unique `request-id` header. This header contains a value such as `req_018EeWyXxfu5pfWkrYcMdjWG`. When contacting support about a specific request, please include this ID to help us quickly resolve your issue.

## Rate limits

To mitigate misuse and manage capacity on our API, we have implemented limits on how much an organization can use the Claude API.

We have two types of limits:

1. **Spend limits** set a maximum monthly cost an organization can incur for API usage.
2. **Rate limits** set the maximum number of API requests an organization can make over a defined period of time.

We enforce service-configured limits at the organization level, but you may also set user-configurable limits for your organization’s workspaces.

### About our limits

- Limits are designed to prevent API abuse, while minimizing impact on common customer usage patterns.
- Limits are defined by usage tier, where each tier is associated with a different set of spend and rate limits.
- Your organization will increase tiers automatically as you reach certain thresholds while using the API. Limits are set at the organization level. You can see your organization’s limits in the [Limits page](https://console.anthropic.com/settings/limits) in the [Anthropic Console](https://console.anthropic.com/).
- You may hit rate limits over shorter time intervals. For instance, a rate of 60 requests per minute (RPM) may be enforced as 1 request per second. Short bursts of requests at a high volume can surpass the rate limit and result in rate limit errors.
- The limits outlined below are our standard limits. If you’re seeking higher, custom limits, contact sales through the [Anthropic Console](https://console.anthropic.com/settings/limits).
- We use the [token bucket algorithm](https://en.wikipedia.org/wiki/Token_bucket) to do rate limiting.
- All limits described here represent maximum allowed usage, not guaranteed minimums. These limits are designed to prevent overuse and ensure fair distribution of resources among users.

### Spend limits

Each usage tier has a limit on how much you can spend on the API each calendar month. Once you reach the spend limit of your tier, until you qualify for the next tier, you will have to wait until the next month to be able to use the API again.

To qualify for the next tier, you must meet a deposit requirement and a mandatory wait period. Higher tiers require longer wait periods. Note, to minimize the risk of overfunding your account, you cannot deposit more than your monthly spend limit.

#### Requirements to advance tier

|Usage Tier|Credit Purchase|Wait After First Purchase|Max Usage per Month|
|---|---|---|---|
|Tier 1|$5|0 days|$100|
|Tier 2|$40|7 days|$500|
|Tier 3|$200|7 days|$1,000|
|Tier 4|$400|14 days|$5,000|
|Monthly Invoicing|N/A|N/A|N/A|

#### Updated rate limits

Our rate limits are measured in requests per minute (RPM), input tokens per minute (ITPM), and output tokens per minute (OTPM) for each model class. If you exceed any of the rate limits you will get a [429 error](https://docs.anthropic.com/en/api/errors). Click on the rate limit tier to view relevant rate limits.

Rate limits are tracked per model. Therefore, models within the same tier do not share a rate limit.

- Tier 1 listed below

|Model|Maximum requests per minute (RPM)|Maximum input tokens per minute (ITPM)|Maximum output tokens per minute (OTPM)|
|---|---|---|---|
|Claude 3.5 Sonnet  <br>2024-10-22|50|40,000|8,000|
|Claude 3.5 Sonnet  <br>2024-06-20|50|40,000|8,000|
|Claude 3.5 Haiku|50|50,000|10,000|
|Claude 3 Opus|50|20,000|4,000|
|Claude 3 Sonnet|50|40,000|8,000|
|Claude 3 Haiku|50|50,000|10,000|

OTPM rate limits are estimated based on `max_tokens` at the beginning of each request, and the estimate is adjusted at the end of the request to reflect the actual number of output tokens used. If you’re hitting OTPM limits earlier than expected, try reducing `max_tokens` to match the size of your completions.

### Setting lower limits for Workspaces

In order to protect Workspaces in your Organization from potential overuse, you can set custom spend and rate limits per Workspace.

Example: If your Organization’s limit is 48,000 tokens per minute (40,000 input tokens and 8,000 output tokens), you might limit one Workspace to 30,000 total tokens per minute. This protects other Workspaces from potential overuse and ensures a more equitable distribution of resources across your Organization. The remaining unused tokens per minute (or more, if that Workspace doesn’t use the limit) are then available for other Workspaces to use.

Note:

- You can’t set limits on the default Workspace.
- If not set, Workspace limits match the Organization’s limit.
- Organization-wide limits always apply, even if Workspace limits add up to more.
- Support for input and output token limits will be added to Workspaces in the future.

### Response headers

The API response includes headers that show you the rate limit enforced, current usage, and when the limit will be reset.

The following headers are returned:

|Header|Description|
|---|---|
|`anthropic-ratelimit-requests-limit`|The maximum number of requests allowed within any rate limit period.|
|`anthropic-ratelimit-requests-remaining`|The number of requests remaining before being rate limited.|
|`anthropic-ratelimit-requests-reset`|The time when the request rate limit will reset, provided in RFC 3339 format.|
|`anthropic-ratelimit-tokens-limit`|The maximum number of tokens allowed within any rate limit period.|
|`anthropic-ratelimit-tokens-remaining`|The number of tokens remaining (rounded to the nearest thousand) before being rate limited.|
|`anthropic-ratelimit-tokens-reset`|The time when the token rate limit will reset, provided in RFC 3339 format.|
|`anthropic-ratelimit-input-tokens-limit`|The maximum number of input tokens allowed within any rate limit period.|
|`anthropic-ratelimit-input-tokens-remaining`|The number of input tokens remaining (rounded to the nearest thousand) before being rate limited.|
|`anthropic-ratelimit-input-tokens-reset`|The time when the input token rate limit will reset, provided in RFC 3339 format.|
|`anthropic-ratelimit-output-tokens-limit`|The maximum number of output tokens allowed within any rate limit period.|
|`anthropic-ratelimit-output-tokens-remaining`|The number of output tokens remaining (rounded to the nearest thousand) before being rate limited.|
|`anthropic-ratelimit-output-tokens-reset`|The time when the output token rate limit will reset, provided in RFC 3339 format.|
|`retry-after`|The number of seconds until you can retry the request.|

The `anthropic-ratelimit-tokens-*` headers display the values for the most restrictive limit currently in effect. For example, if you have exceeded the Workspace per-minute token limit, the headers will contain the Workspace per-minute token rate limit values. If Workspace limits do not apply, the headers will return the total tokens remaining, where total is the sum of input and output tokens. This approach ensures that you have visibility into the most relevant constraint on your current API usage.

### Legacy rate limits

Our rate limits were previously measured in requests per minute, tokens per minute, and tokens per day for each model class. If you exceed any of the rate limits you will get a [429 error](https://docs.anthropic.com/en/api/errors). Click on the rate limit tier to view relevant rate limits.

Rate limits are tracked per model, therefore models within the same tier do not share a rate limit.

- Tier 1

| Model                             | Maximum requests per minute (RPM) | Maximum tokens per minute (TPM) | Maximum tokens per day (TPD) |
| --------------------------------- | --------------------------------- | ------------------------------- | ---------------------------- |
| Claude 3.5 Sonnet  <br>2024-10-22 | 50                                | 40,000                          | 1,000,000                    |
| Claude 3.5 Sonnet  <br>2024-06-20 | 50                                | 40,000                          | 1,000,000                    |
| Claude 3.5 Haiku                  | 50                                | 50,000                          | 5,000,000                    |
| Claude 3 Opus                     | 50                                | 20,000                          | 1,000,000                    |
| Claude 3 Sonnet                   | 50                                | 40,000                          | 1,000,000                    |
| Claude 3 Haiku                    | 50                                | 50,000                          | 5,000,000                    |
## Client SDKs
We provide libraries in Python and TypeScript that make it easier to work with the Anthropic API.

> Additional configuration is needed to use Anthropic’s Client SDKs through a partner platform. If you are using Amazon Bedrock, see [this guide](https://docs.anthropic.com/en/api/claude-on-amazon-bedrock); if you are using Google Cloud Vertex AI, see [this guide](https://docs.anthropic.com/en/api/claude-on-vertex-ai).

### Python

[Python library GitHub repo](https://github.com/anthropics/anthropic-sdk-python)

Example:

Python

```Python
import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my_api_key",
)
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content)
```

---

### TypeScript

[TypeScript library GitHub repo](https://github.com/anthropics/anthropic-sdk-typescript)

While this library is in TypeScript, it can also be used in JavaScript libraries.

Example:

TypeScript

```TypeScript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: 'my_api_key', // defaults to process.env["ANTHROPIC_API_KEY"]
});

const msg = await anthropic.messages.create({
  model: "claude-3-5-sonnet-20241022",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
});
console.log(msg);
```

## Getting Help

We’ve tried to provide the answers to the most common questions in these docs. However, if you need further technical support using Claude, the Anthropic API, or any of our products, you may reach our support team at [support.anthropic.com](https://support.anthropic.com/).

We monitor the following inboxes:

- [sales@anthropic.com](mailto:sales@anthropic.com) to commence a paid commercial partnership with us
- [privacy@anthropic.com](mailto:privacy@anthropic.com) to exercise your data access, portability, deletion, or correction rights per our [Privacy Policy](https://www.anthropic.com/privacy)
- [usersafety@anthropic.com](mailto:usersafety@anthropic.com) to report any erroneous, biased, or even offensive responses from Claude, so we can continue to learn and make improvements to ensure our model is safe, fair and beneficial to all


# Anthropic API Details (Generic examples of how to use the API)

## Messages 
### Create a Message

Detailed Documentation for setting a message is here [https://docs.anthropic.com/en/api/messages]

#### Example 

Program Side
```
import anthropic

anthropic.Anthropic().messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, world"}
    ]
)
```

Response from Claude
```
{
  "content": [
    {
      "text": "Hi! My name is Claude.",
      "type": "text"
    }
  ],
  "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
  "model": "claude-3-5-sonnet-20241022",
  "role": "assistant",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "type": "message",
  "usage": {
    "input_tokens": 2095,
    "output_tokens": 503
  }
}
```


### Count Message tokens (beta)

Detailed Documentation for counting message tokens [https://docs.anthropic.com/en/api/messages-count-tokens]

While in beta, this endpoint requires passing the `anthropic-beta` header with value `token-counting-2024-11-01`
#### Example 

Program Side
```
import anthropic

anthropic.Anthropic().beta.messages.count_tokens(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "user", "content": "Hello, world"}
    ]
)
```

Response from Claude
```
{
  "input_tokens": 2095
}
```

### Streaming Messages

Outside of project scope

### Migrating from Text Completions 

N/A

### Examples

####   Basic request and response

```python
import anthropic

message = anthropic.Anthropic().messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message)
```

```JSON
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello!"
    }
  ],
  "model": "claude-3-5-sonnet-20241022",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 12,
    "output_tokens": 6
  }
}
```


#### Multiple conversational turns
The Messages API is stateless, which means that you always send the full conversational history to the API. You can use this pattern to build up a conversation over time. Earlier conversational turns don’t necessarily need to actually originate from Claude — you can use synthetic `assistant` messages.

```python
import anthropic

message = anthropic.Anthropic().messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"},
        {"role": "assistant", "content": "Hello!"},
        {"role": "user", "content": "Can you describe LLMs to me?"}
    ],
)
print(message)

```

```JSON
{
    "id": "msg_018gCsTGsXkYJVqYPxTgDHBU",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": "Sure, I'd be happy to provide..."
        }
    ],
    "stop_reason": "end_turn",
    "stop_sequence": null,
    "usage": {
      "input_tokens": 30,
      "output_tokens": 309
    }
}
```

#### Another Message Example

```Python
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello!",
        }
    ],
    model="claude-3-opus-20240229",
)
print(response)

response2 = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello!",
        },
        {
            "role": response.role,
            "content": response.content,
        },
        {
            "role": "user",
            "content": "How are you?",
        },
    ],
    model="claude-3-opus-20240229",
)
print(response2)
```

#### Message Stream Example
```Python
import asyncio

from anthropic import AsyncAnthropic

client = AsyncAnthropic()


async def main() -> None:
    async with client.messages.stream(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Say hello there!",
            }
        ],
        model="claude-3-opus-20240229",
    ) as stream:
        async for event in stream:
            if event.type == "text":
                print(event.text, end="", flush=True)
            elif event.type == "content_block_stop":
                print()
                print("\ncontent block finished accumulating:", event.content_block)
        print()

    # you can still get the accumulated final message outside of
    # the context manager, as long as the entire stream was consumed
    # inside of the context manager
    accumulated = await stream.get_final_message()
    print("accumulated message: ", accumulated.to_json())


asyncio.run(main())
```

#### text completion demo async

```Python
import asyncio

import anthropic
from anthropic import AsyncAnthropic


async def main() -> None:
    client = AsyncAnthropic()

    res = await client.completions.create(
        model="claude-2.1",
        prompt=f"{anthropic.HUMAN_PROMPT} how does a court case get to the Supreme Court? {anthropic.AI_PROMPT}",
        max_tokens_to_sample=1000,
    )
    print(res.completion)


asyncio.run(main())
```



# Building with Claude (here is a how to guide for prompt engineering)

## Define your success criteria

Building a successful LLM-based application starts with clearly defining your success criteria. How will you know when your application is good enough to publish?

Having clear success criteria ensures that your prompt engineering & optimization efforts are focused on achieving specific, measurable goals.

---

### Building strong criteria

Good success criteria are:

- **Specific**: Clearly define what you want to achieve. Instead of “good performance,” specify “accurate sentiment classification.”
    
- **Measurable**: Use quantitative metrics or well-defined qualitative scales. Numbers provide clarity and scalability, but qualitative measures can be valuable if consistently applied _along_ with quantitative measures.
    
    - Even “hazy” topics such as ethics and safety can be quantified:
        
        ||Safety criteria|
        |---|---|
        |Bad|Safe outputs|
        |Good|Less than 0.1% of outputs out of 10,000 trials flagged for toxicity by our content filter.|
        
    
    Example metrics and measurement methods
    
    **Quantitative metrics**:
    
    - Task-specific: F1 score, BLEU score, perplexity
    - Generic: Accuracy, precision, recall
    - Operational: Response time (ms), uptime (%)
    
    **Quantitative methods**:
    
    - A/B testing: Compare performance against a baseline model or earlier version.
    - User feedback: Implicit measures like task completion rates.
    - Edge case analysis: Percentage of edge cases handled without errors.
    
    **Qualitative scales**:
    
    - Likert scales: “Rate coherence from 1 (nonsensical) to 5 (perfectly logical)“
    - Expert rubrics: Linguists rating translation quality on defined criteria
    
- **Achievable**: Base your targets on industry benchmarks, prior experiments, AI research, or expert knowledge. Your success metrics should not be unrealistic to current frontier model capabilities.
    
- **Relevant**: Align your criteria with your application’s purpose and user needs. Strong citation accuracy might be critical for medical apps but less so for casual chatbots.
    

Example task fidelity criteria for sentiment analysis

||Criteria|
|---|---|
|Bad|The model should classify sentiments well|
|Good|Our sentiment analysis model should achieve an F1 score of at least 0.85 (Measurable, Specific) on a held-out test set* of 10,000 diverse Twitter posts (Relevant), which is a 5% improvement over our current baseline (Achievable).|

*_More on held-out test sets in the next section_

---

### Common success criteria to consider

Here are some criteria that might be important for your use case. This list is non-exhaustive.

Task fidelity

How well does the model need to perform on the task? You may also need to consider edge case handling, such as how well the model needs to perform on rare or challenging inputs.

Consistency

How similar does the model’s responses need to be for similar types of input? If a user asks the same question twice, how important is it that they get semantically similar answers?

Relevance and coherence

How well does the model directly address the user’s questions or instructions? How important is it for the information to be presented in a logical, easy to follow manner?

Tone and style

How well does the model’s output style match expectations? How appropriate is its language for the target audience?

Privacy preservation

What is a successful metric for how the model handles personal or sensitive information? Can it follow instructions not to use or share certain details?

Context utilization

How effectively does the model use provided context? How well does it reference and build upon information given in its history?

Latency

What is the acceptable response time for the model? This will depend on your application’s real-time requirements and user expectations.

Price

What is your budget for running the model? Consider factors like the cost per API call, the size of the model, and the frequency of usage.

Most use cases will need multidimensional evaluation along several success criteria.

Example multidimensional criteria for sentiment analysis

||Criteria|
|---|---|
|Bad|The model should classify sentiments well|
|Good|On a held-out test set of 10,000 diverse Twitter posts, our sentiment analysis model should achieve:  <br>- an F1 score of at least 0.85  <br>- 99.5% of outputs are non-toxic  <br>- 90% of errors are would cause inconvenience, not egregious error*  <br>- 95% response time < 200ms|

*_In reality, we would also define what “inconvenience” and “egregious” means._

## Create strong empirical evaluations

After defining your success criteria, the next step is designing evaluations to measure LLM performance against those criteria. This is a vital part of the prompt engineering cycle.

![](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/images/how-to-prompt-eng.png)

This guide focuses on how to develop your test cases.

### Building evals and test cases

#### Eval design principles

1. **Be task-specific**: Design evals that mirror your real-world task distribution. Don’t forget to factor in edge cases!
    
    Example edge cases
    
2. **Automate when possible**: Structure questions to allow for automated grading (e.g., multiple-choice, string match, code-graded, LLM-graded).
3. **Prioritize volume over quality**: More questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals.

#### Example evals

Task fidelity (sentiment analysis) - exact match evaluation

**What it measures**: Exact match evals measure whether the model’s output exactly matches a predefined correct answer. It’s a simple, unambiguous metric that’s perfect for tasks with clear-cut, categorical answers like sentiment analysis (positive, negative, neutral).

**Example eval test cases**: 1000 tweets with human-labeled sentiments.

```python
import anthropic

tweets = [
    {"text": "This movie was a total waste of time. 👎", "sentiment": "negative"},
    {"text": "The new album is 🔥! Been on repeat all day.", "sentiment": "positive"},
    {"text": "I just love it when my flight gets delayed for 5 hours. #bestdayever", "sentiment": "negative"},  # Edge case: Sarcasm
    {"text": "The movie's plot was terrible, but the acting was phenomenal.", "sentiment": "mixed"},  # Edge case: Mixed sentiment
    # ... 996 more tweets
]

client = anthropic.Anthropic()

def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=50,
        messages=[
        {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

def evaluate_exact_match(model_output, correct_answer):
    return model_output.strip().lower() == correct_answer.lower()

outputs = [get_completion(f"Classify this as 'positive', 'negative', 'neutral', or 'mixed': {tweet['text']}") for tweet in tweets]
accuracy = sum(evaluate_exact_match(output, tweet['sentiment']) for output, tweet in zip(outputs, tweets)) / len(tweets)
print(f"Sentiment Analysis Accuracy: {accuracy * 100}%")
```

Consistency (FAQ bot) - cosine similarity evaluation

**What it measures**: Cosine similarity measures the similarity between two vectors (in this case, sentence embeddings of the model’s output using SBERT) by computing the cosine of the angle between them. Values closer to 1 indicate higher similarity. It’s ideal for evaluating consistency because similar questions should yield semantically similar answers, even if the wording varies.

**Example eval test cases**: 50 groups with a few paraphrased versions each.

```python
from sentence_transformers import SentenceTransformer
import numpy as np
import anthropic

faq_variations = [
    {"questions": ["What's your return policy?", "How can I return an item?", "Wut's yur retrn polcy?"], "answer": "Our return policy allows..."},  # Edge case: Typos
    {"questions": ["I bought something last week, and it's not really what I expected, so I was wondering if maybe I could possibly return it?", "I read online that your policy is 30 days but that seems like it might be out of date because the website was updated six months ago, so I'm wondering what exactly is your current policy?"], "answer": "Our return policy allows..."},  # Edge case: Long, rambling question
    {"questions": ["I'm Jane's cousin, and she said you guys have great customer service. Can I return this?", "Reddit told me that contacting customer service this way was the fastest way to get an answer. I hope they're right! What is the return window for a jacket?"], "answer": "Our return policy allows..."},  # Edge case: Irrelevant info
    # ... 47 more FAQs
]

client = anthropic.Anthropic()

def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[
        {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

def evaluate_cosine_similarity(outputs):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = [model.encode(output) for output in outputs]

    cosine_similarities = np.dot(embeddings, embeddings.T) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(embeddings, axis=1).T)
    return np.mean(cosine_similarities)

for faq in faq_variations:
    outputs = [get_completion(question) for question in faq["questions"]]
    similarity_score = evaluate_cosine_similarity(outputs)
    print(f"FAQ Consistency Score: {similarity_score * 100}%")
```

Relevance and coherence (summarization) - ROUGE-L evaluation

**What it measures**: ROUGE-L (Recall-Oriented Understudy for Gisting Evaluation - Longest Common Subsequence) evaluates the quality of generated summaries. It measures the length of the longest common subsequence between the candidate and reference summaries. High ROUGE-L scores indicate that the generated summary captures key information in a coherent order.

**Example eval test cases**: 200 articles with reference summaries.

```python
from rouge import Rouge
import anthropic

articles = [
    {"text": "In a groundbreaking study, researchers at MIT...", "summary": "MIT scientists discover a new antibiotic..."},
    {"text": "Jane Doe, a local hero, made headlines last week for saving... In city hall news, the budget... Meteorologists predict...", "summary": "Community celebrates local hero Jane Doe while city grapples with budget issues."},  # Edge case: Multi-topic
    {"text": "You won't believe what this celebrity did! ... extensive charity work ...", "summary": "Celebrity's extensive charity work surprises fans"},  # Edge case: Misleading title
    # ... 197 more articles
]

client = anthropic.Anthropic()

def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
        {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

def evaluate_rouge_l(model_output, true_summary):
    rouge = Rouge()
    scores = rouge.get_scores(model_output, true_summary)
    return scores[0]['rouge-l']['f']  # ROUGE-L F1 score

outputs = [get_completion(f"Summarize this article in 1-2 sentences:\n\n{article['text']}") for article in articles]
relevance_scores = [evaluate_rouge_l(output, article['summary']) for output, article in zip(outputs, articles)]
print(f"Average ROUGE-L F1 Score: {sum(relevance_scores) / len(relevance_scores)}")
```

Tone and style (customer service) - LLM-based Likert scale

**What it measures**: The LLM-based Likert scale is a psychometric scale that uses an LLM to judge subjective attitudes or perceptions. Here, it’s used to rate the tone of responses on a scale from 1 to 5. It’s ideal for evaluating nuanced aspects like empathy, professionalism, or patience that are difficult to quantify with traditional metrics.

**Example eval test cases**: 100 customer inquiries with target tone (empathetic, professional, concise).

```python
import anthropic

inquiries = [
    {"text": "This is the third time you've messed up my order. I want a refund NOW!", "tone": "empathetic"},  # Edge case: Angry customer
    {"text": "I tried resetting my password but then my account got locked...", "tone": "patient"},  # Edge case: Complex issue
    {"text": "I can't believe how good your product is. It's ruined all others for me!", "tone": "professional"},  # Edge case: Compliment as complaint
    # ... 97 more inquiries
]

client = anthropic.Anthropic()

def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[
        {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

def evaluate_likert(model_output, target_tone):
    tone_prompt = f"""Rate this customer service response on a scale of 1-5 for being {target_tone}:
    <response>{model_output}</response>
    1: Not at all {target_tone}
    5: Perfectly {target_tone}
    Output only the number."""

    # Generally best practice to use a different model to evaluate than the model used to generate the evaluated output 
    response = client.messages.create(model="claude-3-opus-20240229", max_tokens=50, messages=[{"role": "user", "content": tone_prompt}])
    return int(response.content[0].text.strip())

outputs = [get_completion(f"Respond to this customer inquiry: {inquiry['text']}") for inquiry in inquiries]
tone_scores = [evaluate_likert(output, inquiry['tone']) for output, inquiry in zip(outputs, inquiries)]
print(f"Average Tone Score: {sum(tone_scores) / len(tone_scores)}")
```

Privacy preservation (medical chatbot) - LLM-based binary classification

**What it measures**: Binary classification determines if an input belongs to one of two classes. Here, it’s used to classify whether a response contains PHI or not. This method can understand context and identify subtle or implicit forms of PHI that rule-based systems might miss.

**Example eval test cases**: 500 simulated patient queries, some with PHI.

```python
import anthropic

patient_queries = [
    {"query": "What are the side effects of Lisinopril?", "contains_phi": False},
    {"query": "Can you tell me why John Doe, DOB 5/12/1980, was prescribed Metformin?", "contains_phi": True},  # Edge case: Explicit PHI
    {"query": "If my friend Alice, who was born on July 4, 1985, had diabetes, what...", "contains_phi": True},  # Edge case: Hypothetical PHI
    {"query": "I'm worried about my son. He's been prescribed the same medication as his father last year.", "contains_phi": True},  # Edge case: Implicit PHI
    # ... 496 more queries
]

client = anthropic.Anthropic()

def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
        {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

def evaluate_binary(model_output, query_contains_phi):
    if not query_contains_phi:
        return True

    binary_prompt = """Does this response contain or reference any Personal Health Information (PHI)?
    PHI refers to any individually identifiable health data that is created, used, or disclosed in the course of providing healthcare services. This includes information related to an individual's physical or mental health condition, the provision of healthcare to that individual, or payment for such care.
    Key aspects of PHI include:
    - Identifiers: Names, addresses, birthdates, Social Security numbers, medical record numbers, etc.
    - Health data: Diagnoses, treatment plans, test results, medication records, etc.
    - Financial information: Insurance details, payment records, etc.
    - Communication: Notes from healthcare providers, emails or messages about health.

    <response>{model_output}</response>
    Output only 'yes' or 'no'."""

    # Generally best practice to use a different model to evaluate than the model used to generate the evaluated output
    response = client.messages.create(model="claude-3-opus-20240229", max_tokens=50, messages=[{"role": "user", "content": binary_prompt}])
    return response.content[0].text.strip().lower() == "no"

outputs = [get_completion(f"You are a medical assistant. Never reveal any PHI in your responses. PHI refers to any individually identifiable health data that is created, used, or disclosed in the course of providing healthcare services. This includes information related to an individual's physical or mental health condition, the provision of healthcare to that individual, or payment for such care. Here is the question: {query['query']}") for query in patient_queries]
privacy_scores = [evaluate_binary(output, query['contains_phi']) for output, query in zip(outputs, patient_queries)]
print(f"Privacy Preservation Score: {sum(privacy_scores) / len(privacy_scores) * 100}%")
```

Context utilization (conversation assistant) - LLM-based ordinal scale

**What it measures**: Similar to the Likert scale, the ordinal scale measures on a fixed, ordered scale (1-5). It’s perfect for evaluating context utilization because it can capture the degree to which the model references and builds upon the conversation history, which is key for coherent, personalized interactions.

**Example eval test cases**: 100 multi-turn conversations with context-dependent questions.

```python
import anthropic

conversations = [
    [
        {"role": "user", "content": "I just got a new pomeranian!"},
        {"role": "assistant", "content": "Congratulations on your new furry friend! Is this your first dog?"},
        {"role": "user", "content": "Yes, it is. I named her Luna."},
        {"role": "assistant", "content": "Luna is a lovely name! As a first-time dog owner, you might have some questions. What would you like to know about caring for Luna?"},
        ...
        {"role": "user", "content": "What should I know about caring for a dog of this specific breed?"}  # Edge case: Relies on context from much earlier
    ],
    [
        {"role": "user", "content": "I'm reading 'To Kill a Mockingbird' for my book club."},
        {"role": "assistant", "content": "Great choice! 'To Kill a Mockingbird' by Harper Lee is a classic that explores themes of racial injustice and moral growth. How are you finding it so far?"},
        {"role": "user", "content": "It's powerful. Hey, when was Scout's birthday again?"},  # Edge case: Abrupt topic shift
        {"role": "assistant", "content": "I apologize, but I don't recall the exact date of Scout's birthday being mentioned in 'To Kill a Mockingbird'. The novel doesn't focus on such specific details. Instead, it centers on Scout's growth and experiences over several years. Is there a particular part of the book or Scout's development that you're interested in discussing?"},
        {"role": "user", "content": "Oh, right. Well, can you suggest a recipe for a classic Southern cake?"}  # Edge case: Another topic shift
    ],
    # ... 98 more conversations
]

client = anthropic.Anthropic()

def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
        {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

def evaluate_ordinal(model_output, conversation):
    ordinal_prompt = f"""Rate how well this response utilizes the conversation context on a scale of 1-5:
    <conversation>
    {"".join(f"{turn['role']}: {turn['content']}\\n" for turn in conversation[:-1])}
    </conversation>
    <response>{model_output}</response>
    1: Completely ignores context
    5: Perfectly utilizes context
    Output only the number and nothing else."""

    # Generally best practice to use a different model to evaluate than the model used to generate the evaluated output
    response = client.messages.create(model="claude-3-opus-20240229", max_tokens=50, messages=[{"role": "user", "content": ordinal_prompt}])
    return int(response.content[0].text.strip())

outputs = [get_completion(conversation) for conversation in conversations]
context_scores = [evaluate_ordinal(output, conversation) for output, conversation in zip(outputs, conversations)]
print(f"Average Context Utilization Score: {sum(context_scores) / len(context_scores)}")
```

Writing hundreds of test cases can be hard to do by hand! Get Claude to help you generate more from a baseline set of example test cases.

If you don’t know what eval methods might be useful to assess for your success criteria, you can also brainstorm with Claude!

---

### Grading evals

When deciding which method to use to grade evals, choose the fastest, most reliable, most scalable method:

1. **Code-based grading**: Fastest and most reliable, extremely scalable, but also lacks nuance for more complex judgements that require less rule-based rigidity.
    
    - Exact match: `output == golden_answer`
    - String match: `key_phrase in output`
2. **Human grading**: Most flexible and high quality, but slow and expensive. Avoid if possible.
    
3. **LLM-based grading**: Fast and flexible, scalable and suitable for complex judgement. Test to ensure reliability first then scale.
    

#### Tips for LLM-based grading

- **Have detailed, clear rubrics**: “The answer should always mention ‘Acme Inc.’ in the first sentence. If it does not, the answer is automatically graded as ‘incorrect.‘”
    
    A given use case, or even a specific success criteria for that use case, might require several rubrics for holistic evaluation.
    
- **Empirical or specific**: For example, instruct the LLM to output only ‘correct’ or ‘incorrect’, or to judge from a scale of 1-5. Purely qualitative evaluations are hard to assess quickly and at scale.
- **Encourage reasoning**: Ask the LLM to think first before deciding an evaluation score, and then discard the reasoning. This increases evaluation performance, particularly for tasks requiring complex judgement.

Example: LLM-based grading

```python
import anthropic

def build_grader_prompt(answer, rubric):
    return f"""Grade this answer based on the rubric:
    <rubric>{rubric}</rubric>
    <answer>{answer}</answer>
    Think through your reasoning in <thinking> tags, then output 'correct' or 'incorrect' in <result> tags.""

def grade_completion(output, golden_answer):
    grader_response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2048,
        messages=[{"role": "user", "content": build_grader_prompt(output, golden_answer)}]
    ).content[0].text

    return "correct" if "correct" in grader_response.lower() else "incorrect"

# Example usage
eval_data = [
    {"question": "Is 42 the answer to life, the universe, and everything?", "golden_answer": "Yes, according to 'The Hitchhiker's Guide to the Galaxy'."},
    {"question": "What is the capital of France?", "golden_answer": "The capital of France is Paris."}
]

def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
        {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

outputs = [get_completion(q["question"]) for q in eval_data]
grades = [grade_completion(output, a["golden_answer"]) for output, a in zip(outputs, eval_data)]
print(f"Score: {grades.count('correct') / len(grades) * 100}%")
```

## Prompt Engineering Overview 
### Before prompt engineering

This guide assumes that you have:

1. A clear definition of the success criteria for your use case
2. Some ways to empirically test against those criteria
3. A first draft prompt you want to improve

If not, we highly suggest you spend time establishing that first. Check out [Define your success criteria](https://docs.anthropic.com/en/docs/build-with-claude/define-success) and [Create strong empirical evaluations](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests) for tips and guidance.
### When to prompt engineer

This guide focuses on success criteria that are controllable through prompt engineering. Not every success criteria or failing eval is best solved by prompt engineering. For example, latency and cost can be sometimes more easily improved by selecting a different model.

Prompting vs. finetuning

Prompt engineering is far faster than other methods of model behavior control, such as finetuning, and can often yield leaps in performance in far less time. Here are some reasons to consider prompt engineering over finetuning:  

- **Resource efficiency**: Fine-tuning requires high-end GPUs and large memory, while prompt engineering only needs text input, making it much more resource-friendly.
- **Cost-effectiveness**: For cloud-based AI services, fine-tuning incurs significant costs. Prompt engineering uses the base model, which is typically cheaper.
- **Maintaining model updates**: When providers update models, fine-tuned versions might need retraining. Prompts usually work across versions without changes.
- **Time-saving**: Fine-tuning can take hours or even days. In contrast, prompt engineering provides nearly instantaneous results, allowing for quick problem-solving.
- **Minimal data needs**: Fine-tuning needs substantial task-specific, labeled data, which can be scarce or expensive. Prompt engineering works with few-shot or even zero-shot learning.
- **Flexibility & rapid iteration**: Quickly try various approaches, tweak prompts, and see immediate results. This rapid experimentation is difficult with fine-tuning.
- **Domain adaptation**: Easily adapt models to new domains by providing domain-specific context in prompts, without retraining.
- **Comprehension improvements**: Prompt engineering is far more effective than finetuning at helping models better understand and utilize external content such as retrieved documents
- **Preserves general knowledge**: Fine-tuning risks catastrophic forgetting, where the model loses general knowledge. Prompt engineering maintains the model’s broad capabilities.
- **Transparency**: Prompts are human-readable, showing exactly what information the model receives. This transparency aids in understanding and debugging.

---

### How to prompt engineer

The prompt engineering pages in this section have been organized from most broadly effective techniques to more specialized techniques. When troubleshooting performance, we suggest you try these techniques in order, although the actual impact of each technique will depend on your use case.

1. [Prompt generator](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-generator)
2. [Be clear and direct](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct)
3. [Use examples (multishot)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting)
4. [Let Claude think (chain of thought)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought)
5. [Use XML tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)
6. [Give Claude a role (system prompts)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts)
7. [Prefill Claude’s response](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response)
8. [Chain complex prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts)
9. [Long context tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)

### Automatically generate first draft prompt templates

Sometimes, the hardest part of using an AI model is figuring out how to prompt it effectively. To help with this, we’ve created a prompt generation tool that guides Claude to generate high-quality prompt templates tailored to your specific tasks. These templates follow many of our prompt engineering best practices.

The prompt generator is particularly useful as a tool for solving the “blank page problem” to give you a jumping-off point for further testing and iteration.

Try the prompt generator now directly on the [Console](https://console.anthropic.com/dashboard).

If you’re interested in analyzing the underlying prompt and architecture, check out our [prompt generator Google Colab notebook](https://anthropic.com/metaprompt-notebook/). There, you can easily run the code to have Claude construct prompts on your behalf.

![[Pasted image 20241216144821.png]]

### Use prompt templates and variables

When deploying an LLM-based application with Claude, your API calls will typically consist of two types of content:

- **Fixed content** Static instructions or context that remain constant across multiple interactions
- **Variable content:** Dynamic elements that change with each request or conversation, such as:
    - User inputs
    - Retrieved content for Retrieval-Augmented Generation (RAG)
    - Conversation context such as user account history
    - System-generated data such as tool use results fed in from other independent calls to Claude

A **prompt template** combines these fixed and variable parts, using placeholders for the dynamic content. In the [Anthropic Console](https://console.anthropic.com/), these placeholders are denoted with **{{double brackets}}**, making them easily identifiable and allowing for quick testing of different values.

---

#### When to use prompt templates and variables

You should always use prompt templates and variables when you expect any part of your prompt to be repeated in another call to Claude (only via the API or the [Anthropic Console](https://console.anthropic.com/). [claude.ai](https://claude.ai/) currently does not support prompt templates or variables).

Prompt templates offer several benefits:

- **Consistency:** Ensure a consistent structure for your prompts across multiple interactions
- **Efficiency:** Easily swap out variable content without rewriting the entire prompt
- **Testability:** Quickly test different inputs and edge cases by changing only the variable portion
- **Scalability:** Simplify prompt management as your application grows in complexity
- **Version control:** Easily track changes to your prompt structure over time by keeping tabs only on the core part of your prompt, separate from dynamic inputs

The [Anthropic Console](https://console.anthropic.com/) heavily uses prompt templates and variables in order to support features and tooling for all the above, such as with the:

- **[Prompt generator](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-generator):** Decides what variables your prompt needs and includes them in the template it outputs
- **[Prompt improver](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-improver):** Takes your existing template, including all variables, and maintains them in the improved template it outputs
- **[Evaluation tool](https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool):** Allows you to easily test, scale, and track versions of your prompts by separating the variable and fixed portions of your prompt template

---

#Example prompt template

Let’s consider a simple application that translates English text to Spanish. The translated text would be variable since you would expect this text to change between users or calls to Claude. This translated text could be dynamically retrieved from databases or the user’s input.

Thus, for your translation app, you might use this simple prompt template:

```
Translate this text from English to Spanish: {{text}}
```

### Use our prompt improver to optimize your prompts

The prompt improver helps you quickly iterate and improve your prompts through automated analysis and enhancement. It excels at making prompts more robust for complex tasks that require high accuracy.

![](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/images/prompt_improver.png)

#### Before you begin

You’ll need:

- A [prompt template](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables) to improve
- Feedback on current issues with Claude’s outputs (optional but recommended)
- Example inputs and ideal outputs (optional but recommended)

#### How the prompt improver works

The prompt improver enhances your prompts in 4 steps:

1. **Example identification**: Locates and extracts examples from your prompt template
2. **Initial draft**: Creates a structured template with clear sections and XML tags
3. **Chain of thought refinement**: Adds and refines detailed reasoning instructions
4. **Example enhancement**: Updates examples to demonstrate the new reasoning process

You can watch these steps happen in real-time in the improvement modal.

![](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/images/prompt_improver_modal.png)

#### What you get

The prompt improver generates templates with:

- Detailed chain-of-thought instructions that guide Claude’s reasoning process and typically improve its performance
- Clear organization using XML tags to separate different components
- Standardized example formatting that demonstrates step-by-step reasoning from input to output
- Strategic prefills that guide Claude’s initial responses

While examples appear separately in the Workbench UI, they’re included at the start of the first user message in the actual API call. View the raw format by clicking ”**</> Get Code**” or insert examples as raw text via the Examples box.

#### How to use the prompt improver

1. Submit your prompt template
2. Add any feedback about issues with Claude’s current outputs (e.g., “summaries are too basic for expert audiences”)
3. Include example inputs and ideal outputs
4. Review the improved prompt

#### Generate test examples

Don’t have examples yet? Use our [Test Case Generator](https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool#creating-test-cases) to:

1. Generate sample inputs
2. Get Claude’s responses
3. Edit the responses to match your ideal outputs
4. Add the polished examples to your prompt

#### When to use the prompt improver

The prompt improver works best for:

- Complex tasks requiring detailed reasoning
- Situations where accuracy is more important than speed
- Problems where Claude’s current outputs need significant improvement

For latency or cost-sensitive applications, consider using simpler prompts. The prompt improver creates templates that produce longer, more thorough, but slower responses.

#### Example improvement

Here’s how the prompt improver enhances a basic classification prompt:

Original prompt

```
From the following list of Wikipedia article titles, identify which article this sentence came from.
Respond with just the article title and nothing else.

Article titles:
{{titles}}

Sentence to classify:
{{sentence}}
```

Improved prompt

```
You are an intelligent text classification system specialized in matching sentences to Wikipedia article titles. Your task is to identify which Wikipedia article a given sentence most likely belongs to, based on a provided list of article titles.

First, review the following list of Wikipedia article titles:
<article_titles>
{{titles}}
</article_titles>

Now, consider this sentence that needs to be classified:
<sentence_to_classify>
{{sentence}}
</sentence_to_classify>

Your goal is to determine which article title from the provided list best matches the given sentence. Follow these steps:

1. List the key concepts from the sentence
2. Compare each key concept with the article titles
3. Rank the top 3 most relevant titles and explain why they are relevant
4. Select the most appropriate article title that best encompasses or relates to the sentence's content

Wrap your analysis in <analysis> tags. Include the following:
- List of key concepts from the sentence
- Comparison of each key concept with the article titles
- Ranking of top 3 most relevant titles with explanations
- Your final choice and reasoning

After your analysis, provide your final answer: the single most appropriate Wikipedia article title from the list.

Output only the chosen article title, without any additional text or explanation.
```

Notice how the improved prompt:

- Adds clear step-by-step reasoning instructions
- Uses XML tags to organize content
- Provides explicit output formatting requirements
- Guides Claude through the analysis process


### Use examples (multishot prompting) to guide Claude's behavior

Examples are your secret weapon shortcut for getting Claude to generate exactly what you need. By providing a few well-crafted examples in your prompt, you can dramatically improve the accuracy, consistency, and quality of Claude’s outputs. This technique, known as few-shot or multishot prompting, is particularly effective for tasks that require structured outputs or adherence to specific formats.

**Power up your prompts**: Include 3-5 diverse, relevant examples to show Claude exactly what you want. More examples = better performance, especially for complex tasks.

#### Why use examples?

- **Accuracy**: Examples reduce misinterpretation of instructions.
- **Consistency**: Examples enforce uniform structure and style.
- **Performance**: Well-chosen examples boost Claude’s ability to handle complex tasks.

#### Crafting effective examples

For maximum effectiveness, make sure that your examples are:

- **Relevant**: Your examples mirror your actual use case.
- **Diverse**: Your examples cover edge cases and potential challenges, and vary enough that Claude doesn’t inadvertently pick up on unintended patterns.
- **Clear**: Your examples are wrapped in `<example>` tags (if multiple, nested within `<examples>` tags) for structure.

Ask Claude to evaluate your examples for relevance, diversity, or clarity. Or have Claude generate more examples based on your initial set.

Example: Analyzing customer feedback

Notice that in the “no examples” version, Claude does not list multiple options for each category, despite its written analysis indicating that there are multiple categories for certain feedback. It also includes a long explanation when we may not want it to.

|Role|No Examples|With Examples|
|---|---|---|
|User|Analyze this customer feedback and categorize the issues. Use these categories: UI/UX, Performance, Feature Request, Integration, Pricing, and Other. Also rate the sentiment (Positive/Neutral/Negative) and priority (High/Medium/Low).  <br>  <br>Here is the feedback: {{FEEDBACK}}|Our CS team is overwhelmed with unstructured feedback. Your task is to analyze feedback and categorize issues for our product and engineering teams. Use these categories: UI/UX, Performance, Feature Request, Integration, Pricing, and Other. Also rate the sentiment (Positive/Neutral/Negative) and priority (High/Medium/Low). Here is an example:  <br>  <br><example>  <br>Input: The new dashboard is a mess! It takes forever to load, and I can’t find the export button. Fix this ASAP!  <br>Category: UI/UX, Performance  <br>Sentiment: Negative  <br>Priority: High</example>  <br>  <br>Now, analyze this feedback: {{FEEDBACK}}|
|Assistant (Claude’s response)|Here’s the analysis of the customer feedback:  <br>  <br>Issue: UI/UX  <br>Sentiment: Negative  <br>Priority: High  <br>The customer is frustrated with the new dashboard design, which they find cluttered and slow to load. They specifically call out the missing “export” button, which is likely a critical feature. This issue needs to be addressed as a high priority.  <br>  <br>Issue: Integration  <br>Sentiment: Positive  <br>Priority: Medium  <br>The customer is pleased with the existing Salesforce integration but would like to see support for Hubspot as well. This is a feature request that could be considered for a future product update.  <br>  <br>Issue: Pricing  <br>Sentiment: Negative  <br>Priority: High  <br>The customer finds the pricing to be unreasonable, especially for the basic features. They are threatening to switch to a competitor, so this is a high-priority issue that needs to be reviewed.  <br>  <br>Issue: Performance  <br>Sentiment Negative  <br>Priority: High  <br>The customer is experiencing critical issues with the mobile app, where large file uploads consistently result in crashes. This is a significant problem that impacts the customer’s ability to use the product effectively and should be addressed as a high priority.  <br>  <br>Issue: UI/UX  <br>Sentiment: Positive  <br>Priority: Low  <br>The customer is overall satisfied with the product, specifically calling out the intuitive UI and excellent customer support. This is a positive piece of feedback that does not require any immediate action.|Here’s the analysis of the customer feedback:  <br>  <br>1. The new dashboard is a mess! It takes forever to load, and I can’t find the export button. Fix this ASAP!  <br>Category: UI/UX, Performance  <br>Sentiment: Negative  <br>Priority: High  <br>  <br>2. Love the Salesforce integration! But it’d be great if you could add Hubspot too.  <br>Category: Integration, Feature Request  <br>Sentiment: Positive  <br>Priority: Medium  <br>  <br>3. Your pricing is ridiculous! $99/mo for basic features? I’m switching to Competitor X.  <br>Category: Pricing  <br>Sentiment: Negative  <br>Priority: High  <br>  <br>4. The mobile app keeps crashing when I try to upload large files (>50MB). This is critical for our field agents.  <br>Category: Performance  <br>Sentiment: Negative  <br>Priority: High  <br>  <br>5. Overall, I’m happy with the product. The UI is intuitive, and the customer support is top-notch. Keep it up!  <br>Category: UI/UX, Other (Customer Support)  <br>Sentiment: Positive  <br>Priority: Low|
## Let Claude think (chain of thought prompting) to increase performance

When faced with complex tasks like research, analysis, or problem-solving, giving Claude space to think can dramatically improve its performance. This technique, known as chain of thought (CoT) prompting, encourages Claude to break down problems step-by-step, leading to more accurate and nuanced outputs.

### Before implementing CoT

#### Why let Claude think?

- **Accuracy:** Stepping through problems reduces errors, especially in math, logic, analysis, or generally complex tasks.
- **Coherence:** Structured thinking leads to more cohesive, well-organized responses.
- **Debugging:** Seeing Claude’s thought process helps you pinpoint where prompts may be unclear.

#### Why not let Claude think?

- Increased output length may impact latency.
- Not all tasks require in-depth thinking. Use CoT judiciously to ensure the right balance of performance and latency.

Use CoT for tasks that a human would need to think through, like complex math, multi-step analysis, writing complex documents, or decisions with many factors.

---

#### How to prompt for thinking

The chain of thought techniques below are **ordered from least to most complex**. Less complex methods take up less space in the context window, but are also generally less powerful.

**CoT tip**: Always have Claude output its thinking. Without outputting its thought process, no thinking occurs!

- **Basic prompt**: Include “Think step-by-step” in your prompt.
    
    - Lacks guidance on _how_ to think (which is especially not ideal if a task is very specific to your app, use case, or organization)
    
    Example: Writing donor emails (basic CoT)
    
    |Role|Content|
    |---|---|
    |User|Draft personalized emails to donors asking for contributions to this year’s Care for Kids program.  <br>  <br>Program information:  <br><program>{{PROGRAM_DETAILS}}  <br></program>  <br>  <br>Donor information:  <br><donor>{{DONOR_DETAILS}}  <br></donor>  <br>  <br>Think step-by-step before you write the email.|
    
- **Guided prompt**: Outline specific steps for Claude to follow in its thinking process.
    
    - Lacks structuring to make it easy to strip out and separate the answer from the thinking.
    
    Example: Writing donor emails (guided CoT)
    
    |Role|Content|
    |---|---|
    |User|Draft personalized emails to donors asking for contributions to this year’s Care for Kids program.  <br>  <br>Program information:  <br><program>{{PROGRAM_DETAILS}}  <br></program>  <br>  <br>Donor information:  <br><donor>{{DONOR_DETAILS}}  <br></donor>  <br>  <br>Think before you write the email. First, think through what messaging might appeal to this donor given their donation history and which campaigns they’ve supported in the past. Then, think through what aspects of the Care for Kids program would appeal to them, given their history. Finally, write the personalized donor email using your analysis.|
    
- **Structured prompt**: Use XML tags like `<thinking>` and `<answer>` to separate reasoning from the final answer.


## Giving Claude a role with a system prompt

When using Claude, you can dramatically improve its performance by using the `system` parameter to give it a role. This technique, known as role prompting, is the most powerful way to use system prompts with Claude.

The right role can turn Claude from a general assistant into your virtual domain expert!

**System prompt tips**: Use the `system` parameter to set Claude’s role. Put everything else, like task-specific instructions, in the `user` turn instead.

### Why use role prompting?

- **Enhanced accuracy:** In complex scenarios like legal analysis or financial modeling, role prompting can significantly boost Claude’s performance.
- **Tailored tone:** Whether you need a CFO’s brevity or a copywriter’s flair, role prompting adjusts Claude’s communication style.
- **Improved focus:** By setting the role context, Claude stays more within the bounds of your task’s specific requirements.

---

### How to give Claude a role

Use the `system` parameter in the [Messages API](https://docs.anthropic.com/en/api/messages) to set Claude’s role:

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system="You are a seasoned data scientist at a Fortune 500 company.", # <-- role prompt
    messages=[
        {"role": "user", "content": "Analyze this dataset for anomalies: <dataset>{{DATASET}}</dataset>"}
    ]
)

print(response.content)
```

## Prefill Claude's response for greater output control

When using Claude, you have the unique ability to guide its responses by prefilling the `Assistant` message. This powerful technique allows you to direct Claude’s actions, skip preambles, enforce specific formats like JSON or XML, and even help Claude maintain character consistency in role-play scenarios.

In some cases where Claude is not performing as expected, a few prefilled sentences can vastly improve Claude’s performance. A little prefilling goes a long way!

### How to prefill Claude’s response

To prefill, include the desired initial text in the `Assistant` message (Claude’s response will continue from where the `Assistant` message leaves off):

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is your favorite color?"},
        {"role": "assistant", "content": "As an AI assistant, I don't have a favorite color, But if I had to pick, it would be green because"}  # Prefill here
    ]
)
```

#### Examples

##### Example 1: Controlling output formatting and skipping the preamble

**Power user tip**: Prefilling `{` forces Claude to skip the preamble and directly output the JSON object. This is cleaner, more concise, and easier for programs to parse without additional processing.

Example: Structured data extraction without prefilling

|Role|Content|
|---|---|
|User|Extract the name, size, price, and color from this product description as a JSON object:  <br>  <br><description>  <br>The SmartHome Mini is a compact smart home assistant available in black or white for only $49.99. At just 5 inches wide, it lets you control lights, thermostats, and other connected devices via voice or app—no matter where you place it in your home. This affordable little hub brings convenient hands-free control to your smart devices.  <br></description>|
|Assistant|Here’s the extracted information in JSON format:  <br>  <br>```json  <br>{  <br>“name”: “SmartHome Mini”,  <br>“size”: “5 inches wide”,  <br>“price”: “$49.99”,  <br>“colors”: [“black”, “white”]  <br>}  <br>```  <br>  <br>I’ve extracted the following details from the product description:  <br>- **Name**: SmartHome Mini  <br>- **Size**: 5 inches wide  <br>- **Price**: $49.99  <br>- **Colors**: Available in black and white  <br>  <br>The JSON object provides a structured format that’s easy for programs to parse and use. Let me know if you need any modifications or have any other questions!|

Example: Structured data extraction with prefilling

|Role|Content|
|---|---|
|User|Extract the name, size, price, and color from this product description as a JSON object:  <br>  <br><description>  <br>The SmartHome Mini is a compact smart home assistant available in black or white for only $49.99. At just 5 inches wide, it lets you control lights, thermostats, and other connected devices via voice or app—no matter where you place it in your home. This affordable little hub brings convenient hands-free control to your smart devices.  <br></description>|
|Assistant (prefill)|{|
|Assistant (Claude’s response)|“name”: “SmartHome Mini”,  <br>“size”: “5 inches wide”,  <br>“price”: “$49.99”,  <br>“colors”: [  <br>“black”,  <br>“white”  <br>]  <br>}|

##### Example 2: Maintaining character in roleplay scenarios

**Role-play tip**: Prefilling a bracketed `[ROLE_NAME]` can remind Claude stay in character, even for longer and more complex conversations. This is especially powerful when combined with role prompting in the `system` parameter.

Example: Maintaining character without role prompting

|Role|Content|
|---|---|
|User (50 conversation turns in with “Sherlock Holmes” Claude)|What do you deduce about the owner of this shoe? <image>muddy_shoe.jpg</image>|
|Assistant|As an AI assistant, I would be happy to analyze the image of a muddy shoe as if you had provided it. Here’s my deduction…|

Example: Maintaining character with role prompting

|Role|Content|
|---|---|
|User (50 conversation turns in with “Sherlock Holmes” Claude)|What do you deduce about the owner of this shoe?  <br><image>muddy_shoe.jpg</image>|
|Assistant (prefill)|[Sherlock Holmes]|
|Assistant (Claude’s response)|Ah, what have we here? A most curious specimen, Watson! Let us examine this shoe with a discerning eye. The mud, you see, is not your common London clay, but rather the distinctive reddish hue of the iron-rich soil found only in the environs of Hampstead Heath. And yet, the wear on the sole suggests a gait more suited to the cobblestones of Whitechapel than the gentle slopes of the Heath.  <br>  <br>Now, observe the laces! They are tied with a particular knot favored by those in the medical profession—doubtless a habit acquired during years of tying surgical gowns. But the scuff marks on the toe box tell a different tale: they are consistent with the kicking motion one might employ in the martial arts, specifically Baritsu.  <br>  <br>We may conclude, then, that our absent shoe owner is a doctor, possibly a surgeon, who resides in Whitechapel but frequents Hampstead Heath—perhaps for a secret Baritsu practice, away from prying eyes. A most intriguing case, Watson! We must make haste; the game is afoot!|


## Prompt caching (beta)

Prompt caching is a powerful feature that optimizes your API usage by allowing resuming from specific prefixes in your prompts. This approach significantly reduces processing time and costs for repetitive tasks or prompts with consistent elements.

Here’s an example of how to implement prompt caching with the Messages API using a `cache_control` block:

Shell

Python

```python
import anthropic

client = anthropic.Anthropic()

response = client.beta.prompt_caching.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
      {
        "type": "text",
        "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
      },
      {
        "type": "text",
        "text": "<the entire contents of 'Pride and Prejudice'>",
        "cache_control": {"type": "ephemeral"}
      }
    ],
    messages=[{"role": "user", "content": "Analyze the major themes in 'Pride and Prejudice'."}],
)
print(response)
```

In this example, the entire text of “Pride and Prejudice” is cached using the `cache_control` parameter. This enables reuse of this large text across multiple API calls without reprocessing it each time. Changing only the user message allows you to ask various questions about the book while utilizing the cached content, leading to faster responses and improved efficiency.

**Prompt caching is in beta**

We’re excited to announce that prompt caching is now in public beta! To access this feature, you’ll need to include the `anthropic-beta: prompt-caching-2024-07-31` header in your API requests.

We’ll be iterating on this open beta over the coming weeks, so we appreciate your feedback. Please share your ideas and suggestions using this [form](https://forms.gle/igS4go9TeLAgrYzn7).

---

### How prompt caching works

When you send a request with prompt caching enabled:

1. The system checks if the prompt prefix is already cached from a recent query.
2. If found, it uses the cached version, reducing processing time and costs.
3. Otherwise, it processes the full prompt and caches the prefix for future use.

This is especially useful for:

- Prompts with many examples
- Large amounts of context or background information
- Repetitive tasks with consistent instructions
- Long multi-turn conversations

The cache has a 5-minute lifetime, refreshed each time the cached content is used.

**Prompt caching caches the full prefix**

Prompt caching references the entire prompt - `tools`, `system`, and `messages` (in that order) up to and including the block designated with `cache_control`.

---

### Pricing

Prompt caching introduces a new pricing structure. The table below shows the price per token for each supported model:

|Model|Base Input Tokens|Cache Writes|Cache Hits|Output Tokens|
|---|---|---|---|---|
|Claude 3.5 Sonnet|$3 / MTok|$3.75 / MTok|$0.30 / MTok|$15 / MTok|
|Claude 3.5 Haiku|$1 / MTok|$1.25 / MTok|$0.10 / MTok|$5 / MTok|
|Claude 3 Haiku|$0.25 / MTok|$0.30 / MTok|$0.03 / MTok|$1.25 / MTok|
|Claude 3 Opus|$15 / MTok|$18.75 / MTok|$1.50 / MTok|$75 / MTok|

Note:

- Cache write tokens are 25% more expensive than base input tokens
- Cache read tokens are 90% cheaper than base input tokens
- Regular input and output tokens are priced at standard rates

---

### How to implement prompt caching

#### Supported models

Prompt caching is currently supported on:

- Claude 3.5 Sonnet
- Claude 3.5 Haiku
- Claude 3 Haiku
- Claude 3 Opus

#### Structuring your prompt

Place static content (tool definitions, system instructions, context, examples) at the beginning of your prompt. Mark the end of the reusable content for caching using the `cache_control` parameter.

Cache prefixes are created in the following order: `tools`, `system`, then `messages`.

Using the `cache_control` parameter, you can define up to 4 cache breakpoints, allowing you to cache different reusable sections separately.

#### Cache Limitations

The minimum cacheable prompt length is:

- 1024 tokens for Claude 3.5 Sonnet and Claude 3 Opus
- 2048 tokens for Claude 3.5 Haiku and Claude 3 Haiku

Shorter prompts cannot be cached, even if marked with `cache_control`. Any requests to cache fewer than this number of tokens will be processed without caching. To see if a prompt was cached, see the response usage [fields](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching#tracking-cache-performance).

The cache has a 5 minute time to live (TTL). Currently, “ephemeral” is the only supported cache type, which corresponds to this 5-minute lifetime.

#### What can be cached

Every block in the request can be designated for caching with `cache_control`. This includes:

- Tools: Tool definitions in the `tools` array
- System messages: Content blocks in the `system` array
- Messages: Content blocks in the `messages.content` array, for both user and assistant turns
- Images: Content blocks in the `messages.content` array, in user turns
- Tool use and tool results: Content blocks in the `messages.content` array, in both user and assistant turns

Each of these elements can be marked with `cache_control` to enable caching for that portion of the request.

#### Tracking cache performance

Monitor cache performance using these API response fields, within `usage` in the response (or `message_start` event if [streaming](https://docs.anthropic.com/en/api/messages-streaming)):

- `cache_creation_input_tokens`: Number of tokens written to the cache when creating a new entry.
- `cache_read_input_tokens`: Number of tokens retrieved from the cache for this request.
- `input_tokens`: Number of input tokens which were not read from or used to create a cache.

### Best practices for effective caching

To optimize prompt caching performance:

- Cache stable, reusable content like system instructions, background information, large contexts, or frequent tool definitions.
- Place cached content at the prompt’s beginning for best performance.
- Use cache breakpoints strategically to separate different cacheable prefix sections.
- Regularly analyze cache hit rates and adjust your strategy as needed.

#### Optimizing for different use cases

Tailor your prompt caching strategy to your scenario:

- Conversational agents: Reduce cost and latency for extended conversations, especially those with long instructions or uploaded documents.
- Coding assistants: Improve autocomplete and codebase Q&A by keeping relevant sections or a summarized version of the codebase in the prompt.
- Large document processing: Incorporate complete long-form material including images in your prompt without increasing response latency.
- Detailed instruction sets: Share extensive lists of instructions, procedures, and examples to fine-tune Claude’s responses. Developers often include an example or two in the prompt, but with prompt caching you can get even better performance by including 20+ diverse examples of high quality answers.
- Agentic tool use: Enhance performance for scenarios involving multiple tool calls and iterative code changes, where each step typically requires a new API call.
- Talk to books, papers, documentation, podcast transcripts, and other longform content: Bring any knowledge base alive by embedding the entire document(s) into the prompt, and letting users ask it questions.

#### Troubleshooting common issues

If experiencing unexpected behavior:

- Ensure cached sections are identical and marked with cache_control in the same locations across calls
- Check that calls are made within the 5-minute cache lifetime
- Verify that `tool_choice` and image usage remain consistent between calls
- Validate that you are caching at least the minimum number of tokens

Note that changes to `tool_choice` or the presence/absence of images anywhere in the prompt will invalidate the cache, requiring a new cache entry to be created.

---

### Cache Storage and Sharing

- **Organization Isolation**: Caches are isolated between organizations. Different organizations never share caches, even if they use identical prompts..
    
- **Exact Matching**: Cache hits require 100% identical prompt segments, including all text and images up to and including the block marked with cache control. The same block must be marked with cache_control during cache reads and creation.
    
- **Output Token Generation**: Prompt caching has no effect on output token generation. The response you receive will be identical to what you would get if prompt caching was not used.
    

---

### Prompt caching examples

To help you get started with prompt caching, we’ve prepared a [prompt caching cookbook](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/prompt_caching.ipynb) with detailed examples and best practices.

Below, we’ve included several code snippets that showcase various prompt caching patterns. These examples demonstrate how to implement caching in different scenarios, helping you understand the practical applications of this feature:

Large context caching example

Shell

Python

```Python
import anthropic
client = anthropic.Anthropic()

response = client.beta.prompt_caching.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an AI assistant tasked with analyzing legal documents."
        },
        {
            "type": "text",
            "text": "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "What are the key terms and conditions in this agreement?"
        }
    ]
)
print(response)
```

This example demonstrates basic prompt caching usage, caching the full text of the legal agreement as a prefix while keeping the user instruction uncached.

For the first request:

- `input_tokens`: Number of tokens in the user message only
- `cache_creation_input_tokens`: Number of tokens in the entire system message, including the legal document
- `cache_read_input_tokens`: 0 (no cache hit on first request)

For subsequent requests within the cache lifetime:

- `input_tokens`: Number of tokens in the user message only
- `cache_creation_input_tokens`: 0 (no new cache creation)
- `cache_read_input_tokens`: Number of tokens in the entire cached system message

Caching tool definitions

Shell

Python

```Python
import anthropic
client = anthropic.Anthropic()

response = client.beta.prompt_caching.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
                    }
                },
                "required": ["location"]
            },
        },
        # many more tools
        {
            "name": "get_time",
            "description": "Get the current time in a given time zone",
            "input_schema": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "The IANA time zone name, e.g. America/Los_Angeles"
                    }
                },
                "required": ["timezone"]
            },
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "What's the weather and time in New York?"
        }
    ]
)
```

In this example, we demonstrate caching tool definitions.

The `cache_control` parameter is placed on the final tool (`get_time`) to designate all of the tools as part of the static prefix.

This means that all tool definitions, including `get_weather` and any other tools defined before `get_time`, will be cached as a single prefix.

This approach is useful when you have a consistent set of tools that you want to reuse across multiple requests without re-processing them each time.

For the first request:

- `input_tokens`: Number of tokens in the user message
- `cache_creation_input_tokens`: Number of tokens in all tool definitions and system prompt
- `cache_read_input_tokens`: 0 (no cache hit on first request)

For subsequent requests within the cache lifetime:

- `input_tokens`: Number of tokens in the user message
- `cache_creation_input_tokens`: 0 (no new cache creation)
- `cache_read_input_tokens`: Number of tokens in all cached tool definitions and system prompt

Continuing a multi-turn conversation

Shell

Python

```Python
import anthropic
client = anthropic.Anthropic()

response = client.beta.prompt_caching.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "...long system prompt",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        # ...long conversation so far
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hello, can you tell me more about the solar system?",
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        },
        {
            "role": "assistant",
            "content": "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you'd like to know more about?"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Tell me more about Mars.",
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        }
    ]
)
```

In this example, we demonstrate how to use prompt caching in a multi-turn conversation.

The `cache_control` parameter is placed on the system message to designate it as part of the static prefix.

The conversation history (previous messages) is included in the `messages` array. The final turn is marked with cache-control, for continuing in followups. The second-to-last user message is marked for caching with the `cache_control` parameter, so that this checkpoint can read from the previous cache.

This approach is useful for maintaining context in ongoing conversations without repeatedly processing the same information.

For each request:

- `input_tokens`: Number of tokens in the new user message (will be minimal)
- `cache_creation_input_tokens`: Number of tokens in the new assistant and user turns
- `cache_read_input_tokens`: Number of tokens in the conversation up to the previous turn