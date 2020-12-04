# Create role for customer
CREATE ROLE 'bookstore_customer';
use bookstore;

GRANT ALL ON auth_group TO 'bookstore_customer';
GRANT ALL ON auth_group_permissions TO 'bookstore_customer';
GRANT ALL ON auth_permissions TO 'bookstore_customer';
GRANT ALL ON auth_user TO 'bookstore_customer';
GRANT ALL ON auth_user_groups TO 'bookstore_customer';
GRANT ALL ON auth_user_user_permissions TO 'bookstore_customer';
GRANT ALL ON django_admin_log TO 'bookstore_customer';
GRANT ALL ON django_content_type TO 'bookstore_customer';
GRANT ALL ON django_migrations TO 'bookstore_customer';
GRANT ALL ON django_session TO 'bookstore_customer';

GRANT ALL ON card TO 'bookstore_customer';
GRANT ALL ON order_item TO 'bookstore_customer';
GRANT ALL ON `order` TO 'bookstore_customer';
GRANT ALL ON customer TO 'bookstore_customer';
GRANT ALL ON payment TO 'bookstore_customer';
GRANT ALL ON review TO 'bookstore_customer';

GRANT SELECT ON author TO 'bookstore_customer';
GRANT SELECT ON book TO 'bookstore_customer';
GRANT SELECT ON book_author TO 'bookstore_customer';
GRANT SELECT ON book_image TO 'bookstore_customer';
GRANT SELECT ON electronic TO 'bookstore_customer';
GRANT SELECT ON traditional TO 'bookstore_customer';
GRANT SELECT ON keyword TO 'bookstore_customer';
GRANT SELECT ON publisher TO 'bookstore_customer';
GRANT SELECT ON staff TO 'bookstore_customer';
GRANT SELECT ON store TO 'bookstore_customer';
GRANT SELECT ON topic TO 'bookstore_customer';





# Create role for staff
CREATE ROLE 'bookstore_staff';
USE bookstore;

GRANT ALL ON auth_group TO 'bookstore_staff';
GRANT ALL ON auth_group_permissions TO 'bookstore_staff';
GRANT ALL ON auth_permissions TO 'bookstore_staff';
GRANT ALL ON auth_user TO 'bookstore_staff';
GRANT ALL ON auth_user_groups TO 'bookstore_staff';
GRANT ALL ON auth_user_user_permissions TO 'bookstore_staff';
GRANT ALL ON django_admin_log TO 'bookstore_staff';
GRANT ALL ON django_content_type TO 'bookstore_staff';
GRANT ALL ON django_migrations TO 'bookstore_staff';
GRANT ALL ON django_session TO 'bookstore_staff';

GRANT ALL ON order_item TO 'bookstore_staff';
GRANT ALL ON `order` TO 'bookstore_staff';
GRANT ALL ON payment TO 'bookstore_staff';
GRANT ALL ON author TO 'bookstore_staff';
GRANT ALL ON book TO 'bookstore_staff';
GRANT ALL ON book_author TO 'bookstore_staff';
GRANT ALL ON book_image TO 'bookstore_staff';
GRANT ALL ON electronic TO 'bookstore_staff';
GRANT ALL ON traditional TO 'bookstore_staff';
GRANT ALL ON keyword TO 'bookstore_staff';
GRANT ALL ON topic TO 'bookstore_staff';
GRANT ALL ON publisher TO 'bookstore_staff';
GRANT ALL ON staff TO 'bookstore_staff';
GRANT ALL ON store TO 'bookstore_staff';
GRANT ALL ON import_history TO 'bookstore_staff';
GRANT ALL ON export_history TO 'bookstore_staff';

GRANT SELECT ON customer TO 'bookstore_staff';
GRANT SELECT ON card TO 'bookstore_staff';
GRANT SELECT ON review TO 'bookstore_staff';




# Grant role for customer and staff
CREATE USER 'customer'@'localhost' IDENTIFIED BY 'Admin.12345';
CREATE USER 'staff'@'localhost' IDENTIFIED BY 'Admin.12345';
USE bookstore;

GRANT 'bookstore_customer' TO 'customer'@'localhost';
GRANT 'bookstore_staff' TO 'staff'@'localhost';