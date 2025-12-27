# User Authentication Specification

## Overview

This specification describes the user authentication system for the application.

## Requirements

### Functional Requirements

- Users can register with email and password
- Users can login with credentials
- Users can reset password

### Non-Functional Requirements

- System must be secure
- Response time < 2 seconds

## User Stories

- As a user, I want to register so that I can access the system
- As a user, I want to login so that I can use features

## Acceptance Criteria

- Registration form validates email format
- Password must be at least 8 characters
- Login returns JWT token
