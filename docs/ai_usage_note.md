# AI Usage Note — Fulfillment Hub

I used AI as a development assistant during the Fulfillment Hub project. I designed, implemented, tested, and refined the application myself, while using AI for targeted technical and documentation support.

## How I Used AI

I used ChatGPT mainly for specific development tasks, debugging, reviewing implementation ideas, and documentation.

Examples include:

* Getting help with Streamlit and Pandas implementation
* Debugging Python and Streamlit issues
* Reviewing filtering, prioritization, and exception-handling logic
* Checking the application against the project requirements
* Getting suggestions for dashboard and operational workflow improvements
* Improving the README and other documentation
* Preparing and refining the video walkthrough

I created the sample data, selected the main operational problems to focus on, tested the application, and made the final product decisions.

## Where I Changed or Disagreed With AI Suggestions

### 1. Focusing on operational problems

During development, I considered different ways of presenting the fulfillment data. I chose not to make the application a generic analytics dashboard with many charts and metrics.

Instead, I focused on the operational problems that could directly affect fulfillment:

* Priority order delay risks
* Inventory shortages and stock transfers
* Courier pickup delays
* SKU / variant verification
* Operational exceptions

This resulted in the Dashboard, Orders, Inventory, and Exceptions pages.

### 2. Recommended actions instead of automatic actions

I also chose to keep the system focused on **recommendations rather than automatic operational execution**.

For example, the application recommends actions such as:

* Escalate fulfillment
* Transfer stock
* Resolve stock shortage
* Contact courier
* Verify SKU / variant

It does not claim to automatically transfer physical stock or contact a courier because the project uses sample data and has no connection to real warehouse or courier systems.

## My Role and AI's Role

AI helped me speed up development, troubleshoot specific issues, and review ideas. I made the final decisions about the product scope, workflow, interface, and operational logic.

The final application follows the workflow:

**Problem → Visibility → Priority → Recommended Action**
