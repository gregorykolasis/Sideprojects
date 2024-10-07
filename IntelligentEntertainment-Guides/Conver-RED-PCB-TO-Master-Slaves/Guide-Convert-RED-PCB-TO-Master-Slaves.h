// Μετατροπη απο PCB κοκκινη παλια , σε Master & Slaves συστημα καλωδιωμενο πανω στον Πινακα 
// Παράδειγμα μετατροπής στο Heilbronn στο Bar

Υπολογίζω πόσα PCB χρησιμοποιει ο κωδικας ->
PCB1,PCB2,PCB3,PCB4,PCB5,PCB6,PCB7,PCB8,PCB9,PCB12,PCB13,PCB14,PCB15,PCB16,PCB17,PCB18,PCB19,PCB20 -> Αρα 17 Πλακετακια

Υπολογισμός Inputs 6*17 = Μέγιστα 102 Inputs αν , ολα τα PCB ειναι συμπληρωμενα
		Όμως ψαχνοντας τον κωδικα κατευθειαν να δω ποια χρησιμοποιουνται βρίσκω
		-> 60 Inputs

Υπολογισμός Outputs 
		 18 Relays 
		 + 11 Mosfets //Συνολικά 29 Outputs
		 + 14 Leds
		 = 42 Outputs
		 
Αρα θα χρειαστώ 2 MCPS για Outputs (2*16 = 32) + 10 Outputs που ειχει ηδη πανω ο Slave
Άρα θα χρειαστώ 4 MCPS για Inputs  (4*16 = 64) που καλύπτουν τα 60

Άρα συνολικά 2 Slaves , η μπορώ να σπάσω τα 4 MCPS για Inputs σε 2 Slaves απο 2 MCP
Στο συγκεκριμενο παραδειγμα επιλέγω 2 Slaves

////--------------------------------------------------------------------S1---------------------------------------------------------------------//

Slave 1 -> (4 MCP για INPUTS)

GPIO1->PCB4_3 Ledstrip WS

OUTPUTS
OUT1->PCB20_1 (1Red)
OUT2->PCB20_2 (2Green) 
OUT3->PCB20_3 (3Red)
OUT4->PCB20_4 (4Green)
OUT5->PCB20_5 (5Red)
OUT6->PCB20_6 (6Green)
OUT7->PCB9_1  (Led1)
OUT8->PCB9_2  (Led2)
OUT9->PCB9_3  (Led3)
OUT10->PCB9_4 (Led4)

MCP1 -> (ADDR3)
IN1 ->PCB3_1
IN2 ->PCB3_2
IN3 ->PCB3_3
IN4 ->PCB3_4
IN5 ->PCB3_5
IN6 ->PCB3_6

IN7 ->PCB4_1
IN8 ->PCB4_2

IN9 ->PCB5_1

IN10->PCB6_1
IN11->PCB6_2
IN12->PCB6_3
IN13->PCB6_4
IN14->PCB6_5
IN15->PCB6_6
IN16->---

///////////////////////////////////////////////////////////////////////

MCP2 -> (ADDR4)
IN1 ->PCB7_1
IN2 ->PCB7_2
IN3 ->PCB7_3
IN4 ->PCB7_4
IN5 ->PCB7_5

IN6 ->PCB8_1
IN7 ->PCB8_2
IN8 ->PCB8_3
IN9 ->PCB8_4
IN10->PCB8_5
IN11->PCB8_6

IN12->PCB12_1
IN13->PCB12_2
IN14->PCB12_3
IN15->PCB12_4
IN16->PCB12_5

///////////////////////////////////////////////////////////////////////

MCP3 -> (ADDR6)
IN1 ->PCB13_1 (Darts_1)
IN2 ->PCB13_2 (Darts_2)
IN3 ->PCB13_3 (Darts_3)
IN4 ->PCB13_4 (Won't be Used)
IN5 ->PCB13_5 (Won't be Used)
IN6 ->PCB13_6 (Won't be Used)

IN7 ->PCB14_1 (SlotMachine)
IN8 ->PCB14_2 (Coins)
IN9 ->PCB14_3
IN10->PCB14_4
IN11->PCB14_5

IN12->PCB18_1 //PCB17
IN13->PCB18_2 //PCB17
IN14->PCB18_3 //PCB17
IN15->PCB16_5 
IN16->        ------------------------******************************************************** Banned PIN

//////////////////////////////////////////////////////////////////////

MCP4 -> (ADDR7)
IN1 ->PCB15_1
IN2 ->PCB15_2
IN3 ->PCB15_3
IN4 ->PCB15_4
IN5 ->PCB15_5
IN6 ->PCB15_6

IN7 ->PCB16_1
IN8 ->PCB16_2
IN9 ->PCB16_3
IN10->PCB16_4

IN11->PCB19_1
IN12->PCB16_6 
IN13->PCB19_3
IN14->PCB19_4
IN15->PCB19_5
IN16->PCB19_6 (Wont'be Used) --> PCB19_2

///////////////////////////////////////////////////////////////////////

////--------------------------------------------------------------------S1---------------------------------------------------------------------//

Slave 2 -> (2 MCP Outputs)     
INPUTS
GPIO1->PCB2_1
GPIO2->PCB2_2
GPIO3->PCB2_3
GPIO4->PCB2_4
GPIO5->PCB2_5
GPIO6->PCB1_1
GPIO7->PCB1_2
GPIO8->PCB1_3

OUT1->PCB5_2  (AnMachine-Confirm-Led)
OUT2->PCB7_6  (Telephone-Confirm-Led)
OUT3->PCB12_6 (DanceFloor-Confirm-Led)
OUT4->PCB14_6 (Won't be Used)
OUT5->PCB13_4 (Darts-Confirm-Led)
OUT6->////PCB17_2 -->Εχει κενη ΘΕΣΗ για Λεντακι
OUT7->////PCB17_3 -->Εχει κενη ΘΕΣΗ για Λεντακι
OUT8->////PCB17_4 -->Εχει κενη ΘΕΣΗ για Λεντακι
OUT9->
OUT10->

MCP1 -> (ADDR1) - OUTPUTS
IO1 ->REL1
IO2 ->REL2
IO3 ->REL3
IO4 ->REL4(S)
IO5 ->REL5
IO6 ->REL6
IO7 ->REL7     
IO8 ->REL8     
IO9 ->REL9     
IO10->REL10
IO11->REL11(S)
IO12->REL12
IO13->REL13   
IO14->REL14
IO15->REL15(S)
IO16->---

MCP2 -> (ADDR2) - OUTPUTS
IO1 ->PWM_1
IO2 ->PWM_2
IO3 ->PWM_3
IO4 ->PWM_4
IO5 ->PWM_5
IO6 ->PWM_6
IO7 ->PWM_7
IO8 ->PWM_8
IO9 ->PWM_9
IO10->PWM_10
IO11->PWM_11
IO12->REL17 (Preheater)
IO13->REL19 (Fridge2)
IO14->REL20 (Fridge3)
IO15->REL24 (Smoke)
IO16->----


	



