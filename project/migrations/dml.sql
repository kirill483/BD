INSERT INTO
    military_offices(military_office_id, address, user_count)
VALUES
    (
     1,
    'г.Москва, ул.Константина Царева',
    0
    ),
    (
    2,
    'г.Астрахань, ул.Аксакова',
     0
    );


INSERT INTO
    users(user_id, email, hash_password, role)
VALUES
   (
    20,
   'Nadya@mail.ru',
   '$2b$12$WWivymLjMT2MYLQxwY7UsOuU21u52rbPckBK1XB5guOQUC/FlQ0Uu',
    'worker'
    );

INSERT INTO
    workers(user_id, first_name, last_name, military_office_id)
VALUES
   (
    20,
   'Надя',
   'Иванова',
    1
    )
