# 🎬 Fulfillment Hub — Video Walkthrough Script

## 0:00–0:15 — Introduction

> Hi, I’m Kowsik. This is my Fulfillment Hub project, an operations control center designed to monitor orders, inventory, and fulfillment exceptions.

## 0:15–1:20 — Dashboard

> I started with the operational dashboard because the main problem in the scenario is visibility.
>
> The team was managing fulfillment using spreadsheets and shared folders, which made it difficult to quickly identify priority orders, delays, inventory problems, and exceptions.
>
> The dashboard provides an operations snapshot with total orders, high-priority orders, pickup delays, inventory risks, and critical exceptions.
>
> The Action Center highlights the issues that need attention.
>
> The fulfillment pipeline shows where orders currently are in the process, from received and processing through picking, packing, staging, and shipping.
>
> The Priority Work Queue then brings important operational work to the front.

## 1:20–2:15 — Orders

> The Orders page gives the operations team a more detailed view of individual orders.
>
> Orders can be searched and filtered by priority, order status, and pickup status.
>
> The page also shows operational risk and the recommended next action.
>
> I created a Priority Work Queue to bring critical and high-risk active orders to the top.
>
> Completed orders are excluded from this operational queue because they no longer require fulfillment action.
>
> The purpose is to help the team identify which orders need attention instead of manually searching through a spreadsheet.

## 2:15–3:10 — Inventory

> The Inventory page focuses on stock availability and demand.
>
> The application shows main warehouse availability, secondary warehouse availability, open order demand, shortfall, transfer quantity, stock health, and recommended action.
>
> This helps identify cases where stock needs to be transferred from the secondary warehouse to the main warehouse.
>
> It also identifies insufficient-stock situations where the available inventory cannot meet the open order demand.
>
> Search and filters make it easier to find specific SKUs, categories, or required actions.

## 3:10–4:05 — Exceptions

> The Exceptions page provides a centralized queue for operational problems.
>
> This addresses the problem of issues being handled informally and potentially being forgotten.
>
> Each exception has an exception ID, order ID, issue type, severity, status, and recommended action.
>
> The application covers issues such as priority order delay risks, stock transfer requirements, courier pickup delays, SKU or variant verification, and insufficient stock.
>
> The goal is not to automatically execute physical warehouse or courier actions. Instead, the system makes the issue visible and gives the operator a clear recommended next action.

## 4:05–4:40 — Why I Chose These Problems

> I focused on five problems that can directly affect fulfillment.
>
> First, priority order delay risks.
>
> Second, inventory shortages and stock transfers.
>
> Third, courier pickup delays.
>
> Fourth, SKU and variant verification.
>
> And finally, operational exceptions that could otherwise be forgotten.
>
> I chose these because they can create fulfillment blockers or customer-facing errors.
>
> Rather than building a dashboard around every possible metric, I focused on making important operational problems visible, prioritizing them, and providing a clear next action.

## 4:40–5:00 — Closing

> Overall, the Fulfillment Hub follows a simple workflow:
>
> Problem, visibility, priority, and recommended action.
>
> The goal is to help the operations team identify high-impact work earlier and reduce the chance that important orders or exceptions are missed.
>
> Thank you for reviewing my Fulfillment Hub project.
