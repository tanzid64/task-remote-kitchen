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
- [x] Integrate Stripe API for payment processing. You can use the stripe library or any other Django-friendly Stripe package.
- [x] Implement a secure and efficient way to handle payment information, such as using Stripe tokens.
- [x] Create models for orders, including necessary fields such as items, quantity, price, etc.
- [x] Connect the ordering system to the menu, ensuring that users can create orders based on the available menu items.

### API Documentation
[Documented by POSTMAN](https://documenter.getpostman.com/view/32603042/2sAXjRW9kE) 
### After setup the application - created with drf-spectacular
[Download API Schema](http:localhost:8000/api/v1/schema/)
[Swagger Doc](http:localhost:8000/api/v1/schema/swagger-ui/)

### Project Installation Guide

Clone the repo and go to the project root.
```bash
git clone https://github.com/tanzid64/task-remote-kitchen.git
```
```bash
cd task-remote-kitchen/
```
For mac and Linux
Start the docker container: 
```bash
make build
```
```bash
make migrate
```
```bash
make collectstatic
```
```bash
make superuser
```
Make file sometimes might not work in windows. If it does not work the simply copy command from `Makefile` directory or follow the below instructions:
```bash
docker compose -f docker-compose.yml up --build -d --remove-orphans
```
```bash
docker compose -f docker-compose.yml run --rm api python manage.py migrate
```
```bash
docker compose -f docker-compose.yml run --rm api python manage.py collectstatic --no-input --clear
```
```bash
docker compose -f docker-compose.yml run --rm api python manage.py createsuperuser
```
### Set up the .env file

`.env.example > .env`

In your `.env` set the following environment variables:

STRIPE CONFIG FOR PAYMENT
Collect keys from stripe website.
- `STRIPE_SECRET_KEY` : Your Stripe Secret.
- `STRIPE_PUBLISHABLE_KEY` : Your Publishable key.
- `STRIPE_WEBHOOK_SECRET_KEY` : Your Webhook secret.

- `STRIPE_SUCCESS_URL` : Your payment success redirect url.
- `STRIPE_CANCEL_URL` : Your payment cancel redirect url.

3. Go to [localhost:8000](http://localhost:8000).

