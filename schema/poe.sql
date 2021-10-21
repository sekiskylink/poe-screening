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

-- port are the ports of entry
CREATE TABLE ports (
    id SERIAL PRIMARY KEY NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    dhis2_code TEXT NOT NULL,
    dhis2_path TEXT NOT NULL DEFAULT '',
    dhis2_parent TEXT NOT NULL DEFAULT '',
    form_order INT,
    created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ports_idx_name ON ports(name);
CREATE INDEX ports_idx_code ON ports(dhis2_code);

-- just to cache orgunits in DHIS2
CREATE TABLE orgunits(
    id SERIAL PRIMARY KEY NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    dhis2_code TEXT NOT NULL,
    dhis2_level INTEGER NOT NULL,
    dhis2_parent TEXT NOT NULL,
    dhis2_path TEXT NOT NULL,
    created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX orgunits_idx_name ON orgunits(name);
CREATE INDEX orgunits_idx_code ON orgunits(dhis2_code);
CREATE INDEX orgunits_idx_level ON orgunits(dhis2_level);
CREATE INDEX orgunits_idx_parent ON orgunits(dhis2_parent);



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
    fields->>'arrivalOrDeparture' AS arrivalOrDeparture,
    fields->>'nationality' AS nationality,
    fields->>'portOfEntry' AS portOfEntry,
    fields->>'dateOfArrival' AS dateOfArrival,
    fields->>'dateOfDeparture' AS dateOfDeparture,
    fields->>'age' AS age,
    fields->>'sex' AS sex,
    fields->>'ugPhysicalAddress' AS ugPhysicalAddress,
    fields->>'PhoneNumber' AS PhoneNumber,
    fields->>'nextOfKin' AS nextOfKin,
    fields->>'passportNumber' AS passportNumber,
    fields->>'passportExpiryDate' AS passportExpiryDate,
    fields->>'flightOrVesselNumber' AS flightOrVesselNumber,
    fields->>'seatNumber' AS seatNumber,
    fields->>'durationOfStay' AS durationOfStay,
    fields->>'modeOfTransport' AS modeOfTransport,
    fields->>'purposeOfTrip' AS purposeOfTrip,
    fields->>'countryOfResidence' AS countryOfResidence,
    fields->>'countryOfDeparture' AS countryOfDeparture,
    fields->>'travellingTo' AS travellingTo,
    fields->>'freeFromSymptoms' AS freeFromSymptoms,
    fields->>'hasNegativePCRTest' AS hasNegativePCRTest,
    fields->>'pcrTestedDate' AS pcrTestedDate,
    fields->>'dateOfLastCovidVaccination' AS dateOfLastCovidVaccination,
    fields->>'yellowFeverCardNumber' AS yellowFeverCardNumber,
    fields->>'dateOfYellowFeverVaccination' AS dateOfYellowFeverVaccination,
    fields->>'covidVaccinationCertFile' AS covidVaccinationCertFile,
    fields->>'pcrTestFile' AS pcrTestFile
    FROM entries;
