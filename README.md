## TASK-REMOTE-KITCHEN [BACK END DEVELOPER]
### Goal
Design & develop of a simple backend API using Django Rest Framework for a food delivery company, where I am managing multiple restaurants with various locations.

### Table of Content
- Features
- API Documentation
- Project Installation Guide

### Features

The goal is to create a simple Django backend where users can manage restaurants and menus.

**User and Auth**
- [x] Extend the user model to include necessary fields for user profiles.
- [x] Token Based Authentication system using rest_framework default authentication.

**Restaurant and menu**
- [x] Allow owners to create a new restaurant.
- [x] Allow owners & employees to update the details of their restaurant.
- [x] Allow owners & employees to create a new menu for their restaurant.
- [x] Allow owners & employees to update the details of a menu.
- [x] Provide a list of menus for the specified restaurant owned by the authenticated owner.
- [x] Allow owners & employees to create new items for a menu.
- [x] Allow owners & employees to update the details of an item.

**User Roles and Permissions**
- [x] Define user roles for owners and employees.
- [x] Implement permission checks in your APIs to ensure that only authorized users (connected to a specific restaurant) can create, modify, or view the menu and place orders.

**Ordering and Payment**
- [ ] Integrate Stripe API for payment processing. You can use the stripe library or any other Django-friendly Stripe package.
- [ ] Create API endpoints for processing payments.
- [ ] Implement a secure and efficient way to handle payment information, such as using Stripe tokens.
- [ ] Create models for orders, including necessary fields such as items, quantity, price, etc.
- [ ] Implement APIs for creating and managing orders.
- [ ] Connect the ordering system to the menu, ensuring that users can create orders based on the available menu items.

### Project Installation Guide

1. Clone the repo and go to the project root.
```bash
git clone https:github.com/tanzid64/
```
2. Start the docker container: 
```bash
make build
```
```bash
make migrate
```
```bash
make superuser
```
3. Go to [localhost:8000](http://localhost:8000).

