# Easy Access Control

Easy Access Control is a simple and practical Odoo module for controlling user access at model level.

## Features

- User-based access control
- Model-level restriction
- Block Read access
- Block Create action
- Block Edit action
- Block Delete action
- Admin and superuser bypass
- Active / Inactive rule support
- Notes field for internal reference
- Duplicate rule prevention

## Supported and Tested

This version has been tested with Contact records in Odoo 16.

Tested restrictions:
- Read restriction
- Create restriction
- Edit restriction
- Delete restriction

## How It Works

1. Open Access Control
2. Create a new rule
3. Select the user
4. Select the model
5. Configure permissions:
   - Read
   - Create
   - Write
   - Delete
6. Save the rule

If a permission is disabled, the selected user will be blocked from performing that action.

## Rule Fields

- Active: Enable or disable the rule
- Rule Name: Internal rule name
- User: User to whom the rule applies
- Model: Target model
- Read: Allow or block view access
- Create: Allow or block create action
- Write: Allow or block edit action
- Delete: Allow or block delete action
- Notes: Internal notes for administrators

## Safety Improvements

This version includes:
- Admin bypass for safer management
- Read access restriction support
- Better user-facing restriction messages
- SQL constraint to prevent duplicate rules for the same user and model

## Known Limitation

UI hide options are available in the rule form, but full button hiding is not yet consistently supported across all Odoo views.

Backend restrictions are fully enforced.

## Version

Current stable release:
v16.0.1.1

## Author

Mohan Mathanabalan

## GitHub

https://github.com/mailtomemohan9387/easy_access_control
