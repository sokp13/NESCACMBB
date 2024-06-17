DROP TABLE IF EXISTS player;
CREATE TABLE player(
   ID         INTEGER  NOT NULL PRIMARY KEY 
  ,First_Name VARCHAR(11) NOT NULL
  ,Last_Name  VARCHAR(13) NOT NULL
  ,Number     INTEGER  NOT NULL
  ,Team_Id    VARCHAR(3) NOT NULL
  ,Position   VARCHAR(7) NOT NULL
  ,Class      VARCHAR(9) NOT NULL
  ,Origin     VARCHAR(25) NOT NULL
  ,Country    VARCHAR(24) NOT NULL
  ,Height     INTEGER  NOT NULL
  ,Games      INTEGER  NOT NULL
);

DROP TABLE IF EXISTS totals;
CREATE TABLE totals(
   ID     INTEGER  NOT NULL PRIMARY KEY 
  ,poss   INTEGER  NOT NULL
  ,pts    INTEGER  NOT NULL
  ,ast    INTEGER  NOT NULL
  ,reb    INTEGER  NOT NULL
  ,oreb   INTEGER  NOT NULL
  ,stl    INTEGER  NOT NULL
  ,blk    INTEGER  NOT NULL
  ,tov    INTEGER  NOT NULL
  ,fouls  INTEGER  NOT NULL
  ,fgm    INTEGER  NOT NULL
  ,fga    INTEGER  NOT NULL
  ,threem INTEGER  NOT NULL
  ,threea INTEGER  NOT NULL
  ,ftm    INTEGER  NOT NULL
  ,fta    INTEGER  NOT NULL
);

DROP TABLE IF EXISTS types;
CREATE TABLE types(
   ID          INTEGER  NOT NULL PRIMARY KEY 
  ,iso_poss    INTEGER  NOT NULL
  ,iso_pts     INTEGER  NOT NULL
  ,iso_ppp     NUMERIC(5,3) NOT NULL
  ,iso_fgm     INTEGER  NOT NULL
  ,iso_fga     INTEGER  NOT NULL
  ,iso_fg_pct  NUMERIC(5,3) NOT NULL
  ,iso_efg     NUMERIC(5,3) NOT NULL
  ,iso_to      NUMERIC(5,3) NOT NULL
  ,iso_ft      NUMERIC(5,3) NOT NULL
  ,iso_score   NUMERIC(5,3) NOT NULL
  ,prb_poss    INTEGER  NOT NULL
  ,prb_pts     INTEGER  NOT NULL
  ,prb_ppp     NUMERIC(5,3) NOT NULL
  ,prb_fgm     INTEGER  NOT NULL
  ,prb_fga     INTEGER  NOT NULL
  ,prb_fg      NUMERIC(5,3) NOT NULL
  ,prb_efg     NUMERIC(5,3) NOT NULL
  ,prb_to      NUMERIC(5,3) NOT NULL
  ,prb_ft      NUMERIC(5,3) NOT NULL
  ,prb_score   NUMERIC(5,3) NOT NULL
  ,post_poss   INTEGER  NOT NULL
  ,post_pts    INTEGER  NOT NULL
  ,post_ppp    NUMERIC(5,3) NOT NULL
  ,post_fgm    INTEGER  NOT NULL
  ,post_fga    INTEGER  NOT NULL
  ,post_fg     NUMERIC(5,3) NOT NULL
  ,post_to     NUMERIC(5,3) NOT NULL
  ,post_ft     NUMERIC(5,3) NOT NULL
  ,post_score  NUMERIC(5,3) NOT NULL
  ,roll_poss   INTEGER  NOT NULL
  ,roll_pts    INTEGER  NOT NULL
  ,roll_ppp    NUMERIC(5,3) NOT NULL
  ,roll_fgm    INTEGER  NOT NULL
  ,roll_fga    INTEGER  NOT NULL
  ,roll_fg     NUMERIC(5,3) NOT NULL
  ,roll_efg    NUMERIC(5,3) NOT NULL
  ,roll_to     NUMERIC(5,3) NOT NULL
  ,roll_ft     NUMERIC(5,3) NOT NULL
  ,roll_score  NUMERIC(5,3) NOT NULL
  ,ho_poss     INTEGER  NOT NULL
  ,ho_pts      INTEGER  NOT NULL
  ,ho_ppp      NUMERIC(5,3) NOT NULL
  ,ho_fgm      INTEGER  NOT NULL
  ,ho_fga      INTEGER  NOT NULL
  ,ho_fg       NUMERIC(5,3) NOT NULL
  ,ho_efg      NUMERIC(5,3) NOT NULL
  ,ho_to       NUMERIC(5,3) NOT NULL
  ,ho_ft       NUMERIC(5,3) NOT NULL
  ,ho_score    NUMERIC(5,3) NOT NULL
  ,su_poss     INTEGER  NOT NULL
  ,su_pts      INTEGER  NOT NULL
  ,su_ppp      NUMERIC(5,3) NOT NULL
  ,su_fgm      INTEGER  NOT NULL
  ,su_fga      INTEGER  NOT NULL
  ,su_fg       NUMERIC(5,3) NOT NULL
  ,su_efg      NUMERIC(5,3) NOT NULL
  ,su_score    NUMERIC(5,3) NOT NULL
  ,os_poss     INTEGER  NOT NULL
  ,os_pts      INTEGER  NOT NULL
  ,os_ppp      NUMERIC(5,3) NOT NULL
  ,os_fgm      INTEGER  NOT NULL
  ,os_fga      INTEGER  NOT NULL
  ,os_fg       NUMERIC(5,3) NOT NULL
  ,os_efg      NUMERIC(5,3) NOT NULL
  ,os_to       NUMERIC(5,3) NOT NULL
  ,os_ft       NUMERIC(5,3) NOT NULL
  ,os_score    NUMERIC(5,3) NOT NULL
  ,trans_poss  INTEGER  NOT NULL
  ,trans_pts   INTEGER  NOT NULL
  ,trans_ppp   NUMERIC(5,3) NOT NULL
  ,trans_fgm   INTEGER  NOT NULL
  ,trans_fga   INTEGER  NOT NULL
  ,trans_fg    INTEGER  NOT NULL
  ,trans_efg   NUMERIC(5,3) NOT NULL
  ,trans_to    NUMERIC(5,3) NOT NULL
  ,trans_ft    NUMERIC(5,3) NOT NULL
  ,trans_score NUMERIC(5,3) NOT NULL
  ,cut_poss    INTEGER  NOT NULL
  ,cut_pts     INTEGER  NOT NULL
  ,cut_ppp     NUMERIC(5,3) NOT NULL
  ,cut_fgm     INTEGER  NOT NULL
  ,cut_fga     INTEGER  NOT NULL
  ,cut_fg      NUMERIC(5,3) NOT NULL
  ,cut_efg     NUMERIC(5,3) NOT NULL
  ,cut_to      NUMERIC(5,3) NOT NULL
  ,cut_ft      NUMERIC(5,3) NOT NULL
  ,cut_score   NUMERIC(5,3) NOT NULL
  ,pb_poss     INTEGER  NOT NULL
  ,pb_pts      INTEGER  NOT NULL
  ,pb_ppp      NUMERIC(5,3) NOT NULL
  ,pb_fgm      INTEGER  NOT NULL
  ,pb_fga      INTEGER  NOT NULL
  ,pb_fg       NUMERIC(5,3) NOT NULL
  ,pb_to       NUMERIC(5,3) NOT NULL
  ,pb_ft       NUMERIC(5,3) NOT NULL
  ,pb_score    NUMERIC(5,3) NOT NULL
);

DROP TABLE IF EXISTS perdef;
CREATE TABLE perdef(
   ID              INTEGER  NOT NULL PRIMARY KEY 
  ,pd_poss         INTEGER  NOT NULL
  ,pd_pts          INTEGER  NOT NULL
  ,pd_ppp          NUMERIC(5,3) NOT NULL
  ,pd_fgm          INTEGER  NOT NULL
  ,pd_fga          INTEGER  NOT NULL
  ,pd_fg_pct       NUMERIC(5,3) NOT NULL
  ,pd_efg_pct      NUMERIC(5,3) NOT NULL
  ,pd_score_pct    NUMERIC(5,3) NOT NULL
  ,pd_threefgm     INTEGER  NOT NULL
  ,pd_threefga     INTEGER  NOT NULL
  ,pd_threepct     NUMERIC(5,3) NOT NULL
  ,pd_three_per_fg NUMERIC(4,2) NOT NULL
);