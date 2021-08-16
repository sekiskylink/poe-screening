CREATE TABLE countries (
    id SERIAL PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    alpha_2_code TEXT NOT NULL
);
CREATE INDEX countries_idx_name ON countries(name);
CREATE INDEX countries_idx_alpha2code ON countries(alpha_2_code);

CREATE TABLE airports (
    id SERIAL PRIMARY KEY NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    country_code TEXT NOT NULL DEFAULT '',
    iata_code TEXT NOT NULL DEFAULT '',
    port_type TEXT NOT NULL DEFAULT '',
    created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX airports_idx_iata_code ON airports(iata_code);
CREATE INDEX airports_idx_name ON airports(name);

CREATE TABLE entries (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    fields JSONB NOT NULL DEFAULT '{}'::JSONB,
    submitted BOOLEAN NOT NULL DEFAULT 'f',
    tei TEXT DEFAULT '',
    created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX entries_idx1 ON entries(submitted);
CREATE INDEX entries_idx2 ON entries(created);
CREATE INDEX entries_idx3 ON entries(updated);
CREATE INDEX entries_idx4 ON entries(tei);
CREATE INDEX entries_idx5 ON entries USING GIN (fields);

CREATE VIEW entries_view AS SELECT
    id,
    fields->>'name' AS name,
    fields->>'nationality' AS nationality,
    fields->>'portOfEntry' AS portOfEntry,
    fields->>'dateOfArrival' AS dateOfArrival,
    fields->>'age' AS age,
    fields->>'gender' AS gender,
    fields->>'passportNumber' AS passportNumber,
    fields->>'embarkmentAirport' AS embarkmentAirport,
    fields->>'embarkmentCountry' AS embarkmentCountry,
    fields->>'flightOrVesselNumber' AS flightOrVesselNumber,
    fields->>'countriesVisited' AS countriesVisited,
    fields->>'ugPhysicalAddress' AS ugPhysicalAddress,
    fields->>'durationOfStay' AS durationOfStay,
    fields->>'ugPhoneNumber' AS ugPhoneNumber,
    fields->>'beenToChina' AS beenToChina,
    fields->>'beenToAffectedCountries' AS beenToAffectedCountries,
    fields->>'affectedCountriesVisited' AS affectedCountriesVisited,
    fields->>'hasFever' AS hasFever,
    fields->>'hasHeadache' AS hasHeadache,
    fields->>'hasCough' AS hasCough,
    fields->>'hasSoreThroat' AS hasSoreThroat,
    fields->>'hasFatigue' AS hasFatigue,
    fields->>'hasBreathingDifficulty' AS hasBreathingDifficulty,
    fields->>'hasDiarrhoea' AS hasDiarrhoea,
    fields->>'vomits' AS vomits,
    fields->>'hasBloodInCoughOrStool' AS hasBloodInCoughOrStool,
    fields->>'hasAbdominalPain' AS hasAbdominalPain,
    fields->>'hasSkinRash' AS hasSkinRash,
    fields->>'bleedsFromBodyParts' AS bleedsFromBodyParts,
    fields->>'beenToEbolaAffectedCountry' AS beenToEbolaAffectedCountry
    FROM entries;
