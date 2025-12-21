# A2UI Cross-Spec Binding Guide

**Author:** Manus AI  
**Date:** December 22, 2025  
**Version:** 1.0.0  
**Status:** Knowledge Base Component

---

## 1. Introduction

This guide explains the mechanisms for **cross-spec binding** within the SmartSpec A2UI framework. While UI specifications are declarative and self-contained for implementation, they do not exist in a vacuum. They must interact with other parts of the system, such as backend APIs, business logic services, shared UI components, and global state.

Cross-spec binding is the declarative method for defining these interactions, enabling a UI spec to reference and consume resources from other specifications. This approach maintains the declarative nature of A2UI while allowing for complex, interconnected applications. It ensures that all dependencies are explicit, traceable, and verifiable.

This document will cover the four primary types of cross-spec binding, their underlying concepts, and provide practical examples.

---

## 2. Core Concepts

### 2.1. The Principle of Explicit Dependency

In SmartSpec, all dependencies between different parts of the system must be explicitly declared. This is a core governance principle that prevents implicit coupling and makes the system architecture transparent and auditable. For A2UI, this means a UI spec must formally declare which other specs it depends on.

### 2.2. Spec-as-API

Every specification (UI, API, Logic, State) is treated as a contract or an API. It defines a set of resources (endpoints, functions, components, state variables) that other specs can consume. This "Spec-as-API" model is fundamental to enabling a decoupled, yet integrated, system.

### 2.3. Declarative Binding Syntax

Bindings are defined within the UI spec using a consistent JSON structure. This allows the `smartspec_generate_ui_implementation` workflow to automatically generate the necessary boilerplate code for data fetching, state management, and event handling.

| Binding Type | Purpose | Keywords |
| :--- | :--- | :--- |
| **Data Binding** | Connect to backend APIs | `data_bindings`, `endpoint_ref` |
| **Action Binding** | Connect to business logic services | `logic_bindings`, `service_ref`, `function_ref` |
| **Component Reference** | Reuse UI components from other specs | `imports`, `component_ref` |
| **State Binding** | Connect to global application state | `state_bindings`, `state_ref` |

---

## 3. Data Binding: Connecting to Backend APIs

Data binding links UI components to backend API endpoints defined in an `api-spec.json` file. This is used for fetching data to display and for submitting data from forms.

### 3.1. Example: Booking Form

Consider a booking form that needs to fetch available time slots when a date is selected and submit the form data to create a booking.

**1. API Specification (`specs/api/booking-api.json`):**

```json
{
  "spec_id": "booking-api",
  "endpoints": [
    {
      "id": "get_available_times",
      "path": "/api/bookings/available-times",
      "method": "GET",
      "response": { "times": "array<string>" }
    },
    {
      "id": "create_booking",
      "path": "/api/bookings",
      "method": "POST",
      "response": { "booking_id": "string" }
    }
  ]
}
```

**2. UI Specification (`specs/ui/booking-form.json`):**

```json
{
  "metadata": {
    "api_spec": "specs/api/booking-api.json"
  },
  "components": [
    {
      "id": "booking-form",
      "type": "Form",
      "data_bindings": {
        "load_times": {
          "source": "api",
          "endpoint_ref": "booking-api:get_available_times",
          "trigger": "date_field.onChange",
          "target": "time_field.options"
        },
        "submit_form": {
          "source": "api",
          "endpoint_ref": "booking-api:create_booking",
          "trigger": "form.onSubmit",
          "on_success": "navigate:/confirmation/{{response.booking_id}}"
        }
      }
    }
  ]
}
```

### 3.2. How It Works

1.  **`metadata.api_spec`**: Declares the dependency on the booking API spec.
2.  **`data_bindings`**: This section defines the connections.
3.  **`endpoint_ref`**: A string combining the `spec_id` and the `endpoint_id` (`booking-api:get_available_times`).
4.  **`trigger`**: Specifies the UI event that initiates the API call (e.g., `date_field.onChange`).
5.  **`target`**: Defines where the API response data should be placed (e.g., the `options` of the `time_field`).
6.  **Code Generation**: The implementation workflow generates the necessary `fetch` calls, `useQuery` hooks (for React), or equivalent data-fetching logic, including handling loading and error states.

---

## 4. Action Binding: Connecting to Business Logic

Action binding connects UI events to business logic functions defined in a `logic-spec.json` file. This is used for complex operations that are not simple API calls, such as calculations, multi-step processes, or interactions with third-party services.

### 4.1. Example: Shopping Cart Calculation

Imagine a checkout page where the total price is calculated by a dedicated service that applies discounts and taxes.

**1. Logic Specification (`specs/logic/cart-logic.json`):**

```json
{
  "spec_id": "cart-logic",
  "services": [
    {
      "id": "cart_calculator",
      "functions": [
        {
          "id": "calculate_total",
          "input": { "items": "array", "discount_code": "string" },
          "output": { "total": "number" }
        }
      ]
    }
  ]
}
```

**2. UI Specification (`specs/ui/checkout.json`):**

```json
{
  "metadata": {
    "logic_spec": "specs/logic/cart-logic.json"
  },
  "components": [
    {
      "id": "checkout-summary",
      "type": "Card",
      "logic_bindings": {
        "update_total": {
          "source": "service",
          "service_ref": "cart-logic:cart_calculator",
          "function_ref": "calculate_total",
          "trigger": "cart.onChange",
          "output_mapping": { "total": "total_display.content" }
        }
      }
    },
    {
      "id": "total_display",
      "type": "Text"
    }
  ]
}
```

### 4.2. How It Works

1.  **`logic_bindings`**: Defines the connection to the business logic service.
2.  **`service_ref`** and **`function_ref`**: Pinpoint the exact function to call (`cart-logic:cart_calculator` and `calculate_total`).
3.  **`output_mapping`**: Maps the output of the function to a property of a UI component (the `content` of the `total_display` Text component).
4.  **Code Generation**: The implementation workflow generates a call to the `cart_calculator.calculate_total` function and ensures the UI is updated reactively when the result is available.

---

## 5. Component Reference: Reusing UI Components

Component referencing allows a UI spec to import and use components defined in another UI spec, typically a shared library. This promotes reusability and consistency.

### 5.1. Example: Using a Shared Avatar Component

**1. Shared Library Specification (`specs/ui/shared-components.json`):**

```json
{
  "spec_id": "shared-components",
  "components": [
    {
      "id": "user-avatar",
      "type": "Avatar",
      "export": true,
      "props": { "user_id": "string" }
    }
  ]
}
```

**2. Feature Specification (`specs/ui/profile-page.json`):**

```json
{
  "imports": [
    {
      "spec": "specs/ui/shared-components.json",
      "components": ["user-avatar"]
    }
  ],
  "components": [
    {
      "id": "profile-header",
      "children": [
        {
          "component_ref": "user-avatar",
          "props": { "user_id": "{{current_user.id}}" }
        }
      ]
    }
  ]
}
```

### 5.2. How It Works

1.  **`export: true`**: The `user-avatar` component in the shared library is marked as exportable.
2.  **`imports`**: The profile page spec declares its dependency on the shared library and specifies which component it wants to use.
3.  **`component_ref`**: Instead of `type`, the spec uses `component_ref` to instantiate the imported component.
4.  **Code Generation**: The implementation workflow generates an `import` statement for the `UserAvatar` component and renders it with the specified props.

---

## 6. State Binding: Connecting to Global State

State binding connects UI components to a global or shared state manager, defined in a `state-spec.json` file. This is ideal for managing application-wide state like user authentication or shopping cart contents.

### 6.1. Example: Shopping Cart Icon Badge

**1. State Specification (`specs/state/app-state.json`):**

```json
{
  "spec_id": "app-state",
  "state": {
    "cart": {
      "schema": { "item_count": "number" },
      "actions": { "add_item": { "updates": "item_count" } }
    }
  }
}
```

**2. UI Specification (`specs/ui/header.json`):**

```json
{
  "state_bindings": {
    "app": "specs/state/app-state.json"
  },
  "components": [
    {
      "id": "cart-icon-badge",
      "type": "Badge",
      "state_binding": {
        "count": "{{app.cart.item_count}}"
      }
    }
  ]
}
```

### 6.2. How It Works

1.  **`state_bindings`**: Declares a dependency on the application state spec.
2.  **`state_binding`**: Connects a component property (`count`) to a value in the state tree (`app.cart.item_count`).
3.  **Code Generation**: The implementation workflow generates code that subscribes the component to the specified state slice (e.g., using `useSelector` in Redux or a similar hook in other state management libraries), ensuring the badge updates automatically whenever the cart's item count changes.

---

## 7. Validation and Governance

To ensure the integrity of these bindings, SmartSpec includes a dedicated validation workflow.

### `smartspec_validate_cross_spec_bindings`

This workflow is run before implementation to verify all cross-spec references.

**Command:**
```bash
/smartspec_validate_cross_spec_bindings --spec specs/ui/booking-form.json
```

**Checks Performed:**

-   **Existence:** Verifies that the referenced spec files exist.
-   **Resource Availability:** Checks if the referenced endpoint, function, or component exists within the target spec.
-   **Version Compatibility:** Ensures that the versions of the source and target specs are compatible.
-   **Schema Matching:** Validates that the data schema of the parameters and outputs match between the specs.

This validation step prevents runtime errors and ensures that the entire system remains consistent and well-integrated, even as individual specifications evolve.

---

## 8. Conclusion

Cross-spec binding is a powerful feature that elevates A2UI from a simple UI generation tool to a fully integrated component of the SmartSpec ecosystem. By providing a declarative, verifiable, and type-safe mechanism for connecting UI to data, logic, and state, it enables the development of complex, robust, and maintainable applications.

This approach embodies the core principles of SmartSpec: governance through explicit contracts, automation through code generation, and reliability through validation. It ensures that even as applications grow in complexity, their architecture remains transparent, manageable, and aligned with the single source of truth defined in the specifications.
