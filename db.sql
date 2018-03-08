ALTER TABLE "ProducerCompany" DROP CONSTRAINT IF EXISTS "ProducerCompany_fk0";

ALTER TABLE "JewelryItem" DROP CONSTRAINT IF EXISTS "JewelryItem_fk0";

ALTER TABLE "JewelryItem" DROP CONSTRAINT IF EXISTS "JewelryItem_fk1";

DROP TABLE IF EXISTS "Region";

DROP TABLE IF EXISTS "ProducerCompany";

DROP TABLE IF EXISTS "JewelryShop";

DROP TABLE IF EXISTS "ItemComposition";

DROP TABLE IF EXISTS "JewelryItem";

CREATE TABLE "Region" (
	"id" serial NOT NULL,
	"region_number" integer NOT NULL,
	"region_name" VARCHAR(256) NOT NULL,
	CONSTRAINT Region_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "ProducerCompany" (
	"id" serial NOT NULL,
	"company_name" VARCHAR(1024) NOT NULL,
	"region" integer NOT NULL,
	CONSTRAINT ProducerCompany_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "JewelryShop" (
	"id" serial NOT NULL,
	"address" VARCHAR(1024) NOT NULL,
	"license copy" bytea,
	"schedule day" VARCHAR(255) NOT NULL,
	"schedule time" VARCHAR(255) NOT NULL,
	CONSTRAINT JewelryShop_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "ItemComposition" (
	"id" serial NOT NULL,
	"material" VARCHAR(255) NOT NULL,
	"weight" FLOAT NOT NULL,
	CONSTRAINT ItemComposition_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "JewelryItem" (
	"id" serial NOT NULL,
	"item_type" VARCHAR(255) NOT NULL,
	"item_weight" FLOAT NOT NULL,
	"item_probe" integer NOT NULL,
	"company_producer" integer NOT NULL,
	"item_arrive_date" DATETIME NOT NULL,
	"item_cost" FLOAT NOT NULL,
	"item_composition" integer NOT NULL,
	CONSTRAINT JewelryItem_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);




ALTER TABLE "ProducerCompany" ADD CONSTRAINT "ProducerCompany_fk0" FOREIGN KEY ("region") REFERENCES "Region"("id");



ALTER TABLE "JewelryItem" ADD CONSTRAINT "JewelryItem_fk0" FOREIGN KEY ("company_producer") REFERENCES "ProducerCompany"("id");
ALTER TABLE "JewelryItem" ADD CONSTRAINT "JewelryItem_fk1" FOREIGN KEY ("item_composition") REFERENCES "ItemComposition"("id");
