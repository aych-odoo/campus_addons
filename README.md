# Campus Marketplace

A beginner Odoo tutorial: build, step by step, a small marketplace where
students sell used items (books, phones, cycles) to other students, in the
spirit of OLX or Facebook Marketplace.

It follows the structure of Odoo's official
[Server Framework 101](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101.html)
tutorial, with this app in place of its Real Estate example.

## The app

A student posts an ad with a photo, a title, an asking price, the item's
condition and whether the price is negotiable. Other students make offers.
The seller **accepts** one offer, which marks the listing as **sold** to that
buyer at that price, or **refuses** offers, which deletes them. The seller can
also **cancel** a listing that is still available. Sold and cancelled
listings are hidden by default, and every important event is logged in a
chatter where buyer and seller can talk.

```
Available ──(seller accepts an offer)──▶ Sold
    │
    └──────(seller clicks Cancel)──────▶ Cancelled
```

## Requirements

- Odoo 20.0 (Community is enough) and its PostgreSQL database
- Basic Python and XML

## Installing

1. Clone this repository and add its folder to the `addons_path` of your
   Odoo configuration.
2. Install the module:
   `./odoo-bin -c <your.conf> -d <database> -i campus_market`
3. After each change, restart Odoo and upgrade the module:
   `./odoo-bin -c <your.conf> -d <database> -u campus_market`

## Following along

Every commit is one step of the tutorial and teaches one idea. Its message
explains the **Concept** and what the **Student sees** after the step.

The `main` branch only holds this README. The finished app is on the
`solution` branch, and the code of every step lives in tags: every step
has a tag `chapter-NN-K` (step K of chapter NN), and the tag `chapter-NN`
marks the end of chapter NN (the same commit as its last step).
To follow chapter 7, for example:

```
git tag -l "chapter-07-*"    # list the steps of chapter 7
git checkout chapter-06      # end of chapter 6 = start of chapter 7
git checkout chapter-07-1    # first step of chapter 7
git show                     # what this step changed
git checkout chapter-07-2    # next step, and so on
git checkout solution        # the finished app
git checkout main            # back to the start
```

Upgrade the module after each step. Going back to an earlier step leaves
newer columns in the database, so start from a fresh database when you go
backwards.

## Chapters

Each chapter lists its steps (with their tags), the files it touches, the
Odoo concepts it introduces and the result at the end. File paths are
inside the `campus_market/` folder.

### Chapter 1: Introduction

**Steps**

- `chapter-01-1` Add this README and a `.gitignore` (`__pycache__/`,
  `.vscode/`).

**Files:** `README.md`, `.gitignore` (at the root of the repository)

**Result:** no Odoo module yet.

### Chapter 2: A new application

**Steps**

- `chapter-02-1` Create the `campus_market` folder with an empty
  `__init__.py` and a `__manifest__.py`: name "Campus Marketplace", a
  summary, `"depends": ["base"]`, `"application": True` and
  `"license": "LGPL-3"`.

**Files:** `__init__.py`, `__manifest__.py`

**Concepts:** module structure, the manifest

**Result:** "Campus Marketplace" appears in the Apps menu and installs; it
does nothing yet.

### Chapter 3: Models and basic fields

**Steps**

- `chapter-03-1` Create the `market.listing` model with `name` (Char,
  "Title", required), `description` (Text) and `price` (Float, "Asking
  Price", required). Import the `models` folder from `__init__.py`.
- `chapter-03-2` Add `condition` (Selection: New, Like New, Used),
  `is_negotiable` (Boolean, "Negotiable") and `image` (Image, at most
  1024 × 1024).

**Files:** `__init__.py`, `models/__init__.py`, `models/market_listing.py`

**Concepts:** `models.Model`, `_name`, `_description`, field types,
`required`, `string`

**Result:** a `market_listing` table in the database; nothing in the
interface yet.

### Chapter 4: Security

**Steps**

- `chapter-04-1` Create `security/ir.access.csv` giving internal users
  (`base.group_user`) full access (`crud`) to `market.listing`, and add
  it to the manifest's `data`.

**Files:** `security/ir.access.csv`, `__manifest__.py`

**Concepts:** access rights (`ir.access` in Odoo 20.0), groups

**Result:** users are allowed to work with listings.

### Chapter 5: Actions and menus

**Steps**

- `chapter-05-1` Add a window action for listings (list and form views)
  and the menus "Campus Marketplace" > "Listings". Add both XML files to
  the manifest, with the menus last.

**Files:** `views/market_listing_views.xml`, `views/market_menus.xml`,
`__manifest__.py`

**Concepts:** window actions (`ir.actions.act_window`), `<menuitem>`,
the order of data files

**Result:** the app is on the home screen, and listings can be created
with the screens Odoo generates by default.

### Chapter 6: Basic views

**Steps**

- `chapter-06-1` List view: title, asking price and condition.
- `chapter-06-2` Form view: photo at the top right, title as a heading,
  price, condition and "Negotiable", and a "Description" tab.
- `chapter-06-3` Search view: search by title; filters New, Like New and
  Used; group by condition.

**Files:** `views/market_listing_views.xml`

**Concepts:** `<list>`, `<form>`, `<sheet>`, `<group>`, `<notebook>`,
`<search>`, `<filter>`, domains

**Result:** custom list, form and search for listings.

### Chapter 7: Relations, part 1

**Steps**

- `chapter-07-1` Add the `market.category` model (`name`) with its
  access line, list and form views, an action and a "Configuration >
  Categories" menu.
- `chapter-07-2` Add `category_id` (Many2one to `market.category`) to
  listings; show it in the list, the form and the search (with "Group By
  > Category").
- `chapter-07-3` Add the `market.tag` model (`name`) with its access
  line, an editable list view, an action and a "Configuration > Tags"
  menu. Add `tag_ids` (Many2many to `market.tag`) to listings, shown as
  tags.
- `chapter-07-4` Add `seller_id` (Many2one to `res.users`), filled in
  with the current user by default; show it in the list and the form.

**Files:** `models/market_category.py`, `models/market_tag.py`,
`models/market_listing.py`, `models/__init__.py`,
`security/ir.access.csv`, `views/market_category_views.xml`,
`views/market_tag_views.xml`, `views/market_listing_views.xml`,
`views/market_menus.xml`, `__manifest__.py`

**Concepts:** Many2one, Many2many, `widget="many2many_tags"`,
`editable="bottom"`, default values

**Result:** listings have a category, tags and a seller.

### Chapter 8: Relations, part 2

**Steps**

- `chapter-08-1` Add the `market.offer` model: `partner_id` (Many2one to
  `res.partner`, "Buyer", required), `price` (Float, required) and
  `listing_id` (Many2one to `market.listing`, required), sorted from the
  highest price. Add its access line; it gets no menu.
- `chapter-08-2` Add `offer_ids` (One2many) to listings, and an "Offers"
  tab in the form with an editable list of buyer and price.

**Files:** `models/market_offer.py`, `models/market_listing.py`,
`models/__init__.py`, `security/ir.access.csv`,
`views/market_listing_views.xml`

**Concepts:** One2many, `_order`, editable lists inside a form

**Result:** offers are typed directly into the listing form.

### Chapter 9: Computed fields

**Steps**

- `chapter-09-1` Add `best_offer` (Float), computed as the highest offer
  price (0 when there are no offers), and show it under the asking price.

**Files:** `models/market_listing.py`, `views/market_listing_views.xml`

**Concepts:** `compute=`, `@api.depends`

**Result:** the best offer updates as offers are added or changed.

### Chapter 10: Constraints

**Steps**

- `chapter-10-1` SQL constraints: listing and offer prices must be
  greater than 0; category names and tag names must be unique.
- `chapter-10-2` Python constraint on offers: sellers cannot make an
  offer on their own listing, and on a listing that is not negotiable an
  offer must be at least the asking price.

**Files:** `models/market_listing.py`, `models/market_offer.py`,
`models/market_category.py`, `models/market_tag.py`

**Concepts:** `models.Constraint`, `@api.constrains`, `ValidationError`

**Result:** wrong prices, duplicate names and invalid offers are refused
with a message.

### Chapter 11: Closing the deal

**Steps**

- `chapter-11-1` Add `state` (Available, Sold, Cancelled; Available by
  default), `buyer_id` and `selling_price`, all read-only. Show the state
  as a status bar, and the buyer and price in a "Sale" section.
- `chapter-11-2` Add Accept and Refuse buttons to each offer. Accept
  marks the listing as Sold with the offer's buyer and price; Refuse
  deletes the offer.
- `chapter-11-3` Add a Cancel button to the listing form.
- `chapter-11-4` Hide the buttons and the "Sale" section when they don't
  apply, and lock the offers once a listing is sold or cancelled.
- `chapter-11-5` Add Available, Sold and Cancelled filters, "Group By >
  State" and a State column; open Listings with only the available ones.
- `chapter-11-6` Refuse new or changed offers on listings that are no
  longer available.

**Files:** `models/market_listing.py`, `models/market_offer.py`,
`views/market_listing_views.xml`

**Concepts:** `<header>`, `widget="statusbar"`, `<button type="object">`,
`UserError`, `invisible` and `readonly` conditions, `parent.`,
`search_default_` in the action context

**Result:** the full life cycle of a listing: available, then sold or
cancelled.

### Chapter 12: Interacting with other modules

**Steps**

- `chapter-12-1` Add `mail` to the manifest's `depends`, inherit
  `mail.thread` in listings and add `<chatter/>` to the form.
- `chapter-12-2` Track changes to the asking price and the state.
- `chapter-12-3` Post a message when a listing is sold (and add the
  buyer as a follower) or cancelled.

**Files:** `__manifest__.py`, `models/market_listing.py`,
`models/market_offer.py`, `views/market_listing_views.xml`

**Concepts:** `depends`, `_inherit`, `tracking=True`, `message_post`,
`message_subscribe`

**Result:** every listing has a chatter with its history.
