(define (problem deliver-packages)
    (:domain packages)
    (:objects
        p1 - package
        truck1 - truck
        plane1 - airplane
        port1 - ship

        locA locB locC locD airport1 seaport1 warehouse1 - location
    )

    (:init
        ;; początkowe pozycje
        (at p1 locA)
        (at-vehicle truck1 locA)
        (at-vehicle plane1 airport1)
        (at-vehicle port1 seaport1)

        ;; połączenia drogowe (dwukierunkowe)
        (connected-road locA locB)
        (connected-road locB locA)
        (connected-road locB locC)
        (connected-road locC locB)
        (connected-road locC warehouse1) ; połączenie do warehouse1
        (connected-road warehouse1 locC)

        ;; połączenia między różnymi typami transportu
        (connected-road locA airport1) ; dostęp do lotniska
        (connected-road airport1 locA)
        (connected-road locB seaport1) ; dostęp do portu morskiego
        (connected-road seaport1 locB)

        ;; połączenia lotnicze (dwukierunkowe)
        (connected-air airport1 locC)
        (connected-air locC airport1)

        ;; połączenia morskie (dwukierunkowe)
        (connected-sea seaport1 locD)
        (connected-sea locD seaport1)
        (connected-road locD warehouse1) ; połączenie z locD do warehouse1
        (connected-road warehouse1 locD)

        ;; typy lokalizacji
        (is-airport airport1)
        (is-seaport seaport1)
        (is-warehouse warehouse1)

        ;; funkcje kosztów i czasów (dwukierunkowe)
        (= (travel-cost truck1 locA locB) 5)
        (= (travel-duration truck1 locA locB) 2)
        (= (travel-cost truck1 locB locA) 5)
        (= (travel-duration truck1 locB locA) 2)

        (= (travel-cost truck1 locB locC) 5)
        (= (travel-duration truck1 locB locC) 2)
        (= (travel-cost truck1 locC locB) 5)
        (= (travel-duration truck1 locC locB) 2)

        (= (travel-cost truck1 locC warehouse1) 3)
        (= (travel-duration truck1 locC warehouse1) 1)
        (= (travel-cost truck1 warehouse1 locC) 3)
        (= (travel-duration truck1 warehouse1 locC) 1)

        (= (travel-cost truck1 locA airport1) 2)
        (= (travel-duration truck1 locA airport1) 1)
        (= (travel-cost truck1 airport1 locA) 2)
        (= (travel-duration truck1 airport1 locA) 1)

        (= (travel-cost truck1 locB seaport1) 3)
        (= (travel-duration truck1 locB seaport1) 1)
        (= (travel-cost truck1 seaport1 locB) 3)
        (= (travel-duration truck1 seaport1 locB) 1)

        (= (travel-cost truck1 locD warehouse1) 4)
        (= (travel-duration truck1 locD warehouse1) 2)
        (= (travel-cost truck1 warehouse1 locD) 4)
        (= (travel-duration truck1 warehouse1 locD) 2)

        (= (travel-cost plane1 airport1 locC) 20)
        (= (travel-duration plane1 airport1 locC) 1)
        (= (travel-cost plane1 locC airport1) 20)
        (= (travel-duration plane1 locC airport1) 1)

        (= (travel-cost port1 seaport1 locD) 15)
        (= (travel-duration port1 seaport1 locD) 3)
        (= (travel-cost port1 locD seaport1) 15)
        (= (travel-duration port1 locD seaport1) 3)

        (= (total-cost) 0)
    )

    (:goal
        (and
            (at p1 warehouse1)
        )
    )

    (:metric minimize
        (total-cost)
    )
)