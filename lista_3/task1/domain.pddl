(define (domain packages)

    (:requirements :strips :typing :durative-actions :numeric-fluents :negative-preconditions :conditional-effects :action-costs)

    (:types
        location package vehicle - object
        truck airplane ship - vehicle
    )

    (:predicates
        (at ?p - package ?l - location)
        (in ?p - package ?v - vehicle)
        (at-vehicle ?v - vehicle ?l - location)
        (connected-road ?from ?to - location)
        (connected-air ?from ?to - location)
        (connected-sea ?from ?to - location)
        (is-airport ?l - location)
        (is-seaport ?l - location)
        (is-warehouse ?l - location)
    )

    (:functions
        (total-cost)
        (travel-cost ?v - vehicle ?from - location ?to - location)
        (travel-duration ?v - vehicle ?from ?to - location)
    )

    (:action load
        :parameters (?p - package ?v - vehicle ?l - location)
        :precondition (and (at ?p ?l) (at-vehicle ?v ?l))
        :effect (and (not (at ?p ?l)) (in ?p ?v))
    )

    (:action unload
        :parameters (?p - package ?v - vehicle ?l - location)
        :precondition (and (in ?p ?v) (at-vehicle ?v ?l))
        :effect (and (at ?p ?l) (not (in ?p ?v)))
    )

    (:durative-action drive
        :parameters (?v - truck ?from ?to - location)
        :duration (= ?duration (travel-duration ?v ?from ?to))
        :condition (and
            (at start (at-vehicle ?v ?from))
            (at start (connected-road ?from ?to))
        )
        :effect (and
            (at start (not (at-vehicle ?v ?from)))
            (at end (at-vehicle ?v ?to))
            (at end (increase (total-cost) (travel-cost ?v ?from ?to)))
        )
    )

    (:durative-action fly
        :parameters (?v - airplane ?from ?to - location)
        :duration (= ?duration (travel-duration ?v ?from ?to))
        :condition (and
            (at start (at-vehicle ?v ?from))
            (at start (connected-air ?from ?to))
            (at start (is-airport ?from))
            (at start (is-airport ?to))
        )
        :effect (and
            (at start (not (at-vehicle ?v ?from)))
            (at end (at-vehicle ?v ?to))
            (increase (total-cost) (travel-cost ?v ?from ?to))
        )
    )

    (:durative-action sail
        :parameters (?v - ship ?from ?to - location)
        :duration (= ?duration (travel-duration ?v ?from ?to))
        :condition (and
            (at start (at-vehicle ?v ?from))
            (at start (connected-sea ?from ?to))
            (at start (is-seaport ?from))
            (at start (is-seaport ?to))
        )
        :effect (and
            (at start (not (at-vehicle ?v ?from)))
            (at end (at-vehicle ?v ?to))
            (increase (total-cost) (travel-cost ?v ?from ?to))
        )
    )
)