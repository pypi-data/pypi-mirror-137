Retry Iter - The easy way to handle retries via iteration
=========================================================


This module provides to generator functions, that could be used to handle
retries via iteration. What could be easier then just iterate over attempts?

Take a look at examples below:


Synchronous retry
-----------------


.. code-block:: python

    from retry_iter import retry_iter

    state = False

    for attempt in retry_iter(max_retries=5):
        if do_operation(params):
            state = True
            break

    if not state:
        raise Exception("Operation failed")



Asynchronous retry
------------------


.. code-block:: python

    from retry_iter import a_retry_iter

    state = False

    async for attempt in a_retry_iter(max_retries=5):
        if await do_operation(params):
            state = True
            break

    if not state:
        raise Exception("Operation failed")


Yodoo Cockpit - Manage your odoo infrastructure via odoo
========================================================

.. image:: https://crnd.pro/web/image/18846/banner_2_4_gif_animation_cut.gif
  :target: https://crnd.pro/yodoo-cockpit
  :alt: Yodoo Cockpit - Manage your odoo infrastructure via odoo

Take a look at `Yodoo Cockpit <https://crnd.pro/yodoo-cockpit>`__ project, and discover the easiest way to manage your odoo installation.
Just short notes about `Yodoo Cockpit <https://crnd.pro/yodoo-cockpit>`__:

- start new production-ready odoo instance in 1-2 minutes.
- add custom addons to your odoo instances in 5-10 minutes.
- out-of-the-box email configuration: just press button and add some records to your DNS, and get a working email
- make your odoo instance available to external world (internet) in 30 seconds (just add single record in your DNS)

If you have any questions, then contact us at `info@crnd.pro <mailto:info@crnd.pro>`__, so we could schedule online-demonstration.


Level up your service quality
=============================

Level up your service with our `Helpdesk <https://crnd.pro/solutions/helpdesk>`__ / `Service Desk <https://crnd.pro/solutions/service-desk>`__ / `ITSM <https://crnd.pro/itsm>`__ solution.

Just test it at `yodoo.systems <https://yodoo.systems/saas/templates>`__: choose template you like, and start working.

Test all available features of `Bureaucrat ITSM <https://crnd.pro/itsm>`__ with `this template <https://yodoo.systems/saas/template/bureaucrat-itsm-demo-data-95>`__.
    

Bug tracker
===========

Bugs are tracked on `CR&D's Helpdesk <https://crnd.pro/requests>`__.
In case of trouble, please report there.

Maintainer
==========

.. image:: https://crnd.pro/web/image/3699/300x140/crnd.png
    :target: https://crnd.pro
    :alt: Center of Research & Development

Our web site is: https://crnd.pro/

This module is maintained by the `Center of Research & Development <https://crnd.pro>`__ company.

We can provide you further Odoo Support, Odoo implementation, Odoo customization, Odoo 3rd Party development and integration software, consulting services (more info available on `our site <https://crnd.pro/our-services>`__).Our main goal is to provide the best quality product for you. 

For any questions `contact us <mailto:info@crnd.pro>`__.

