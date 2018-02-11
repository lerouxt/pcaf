
HEADER =  (('case_id',          'STRING'),
           ('form_name',        'STRING'),
           ('initial_visit',    'INT'),
           ('followup_visit',   'INT'),
           ('preipt_visit',     'INT'),
           ('visit_date',       'STRING'),
           ('employment',       'STRING'),
           ('parish',           'STRING'),
           ('age',              'INT'),
           ('tribe',            'STRING'),
           ('religion',         'STRING'),
           ('marital_status',   'STRING'),
           ('num_children',     'INT'),
           ('education_level',  'STRING'),
           ('sub_county',       'STRING'),
           ('district',         'STRING'),
           ('village',          'STRING'),
           ('live_with',        'STRING'),
           ('household_head',   'INT'),
           ('phq2_total',       'INT'),
           ('phq9_9',           'INT'),
           ('phq9_total',       'INT'),
           ('psychoeducation_flag', 'INT'),
           ('functioning_total', 'INT'),

           # following are computed and should match up with COMPUTED_FLAGS
           ('region',            'STRING'),
           ('depressed_flag',    'INT'),
           ('severely_depressed_flag', 'INT'),
           ('suicidal_flag',     'INT')
         )

FORM_MAPPING = {

    #######################################################################
    # Initial Screening for Soroti
    #######################################################################
    "http://openrosa.org/formdesigner/ED17E656-6080-4BE5-8625-461B34531344": {
        'region': 'Soroti!',
        'initial_visit': '1!',
        'followup_visit': '0!',
        'preipt_visit': '0!',
        'case_id': 'case/@case_id',
        'form_name': '@name',
        'visit_date': 'Date',
        'employment': 'Employment',
        'parish': 'Parish',
        'age': 'Age',
        'tribe': 'Tribe?',
        'religion': 'Religion?',
        'marital_status': 'Marital-status',
        'num_children': 'Children-No',
        'education_level': 'Education-level',
        'sub_county': 'Sub-county?',
        'district': 'District?',
        'village': 'Village?',
        'live_with': 'Live-with',
        'household_head': 'Household-Head',
        'phq2_total': 'PHQ2/total_PHQ2',
        'phq9_9': 'phq9/PHQ-9/PHQ9-9',
        'phq9_total': 'phq9/PHQ-9/PHQ9_TOTAL',
        'psychoeducation_flag': 'Functioning/FUNCTIONING/PSYCHOEDUCATION',
        'functioning_total': 'Functioning/FUNCTIONING/Functioning_Total'
    },

#            <Name />
#            <ID />
#            <Date />
#            <District />
#            <Sub-county />
#            <Village />
#            <Parish />
#            <Phone_No />
#            <Age />
#            <Tribe />
#            <question3 />
#            <Religion />
#            <Others />
#            <Marital-status />
#            <Children-No />
#            <Education-level />
#            <Employment />
#            <Others-employment />
#            <Own-home />
#            <Household-Head />
#            <Live-with />
#            <PHQ2>
#                <PHQ2_1 />
#                <PHQ2_2 />
#                <total_PHQ2 />
#                <Total_PHQ2 />
#                <Completed_by />
#                <Thank_to_the_patient />
#            </PHQ2>
#            <phq9>
#                <PHQ-9>
#                    <PHQ9-1 />
#                    <PHQ9-2 />
#                    <PHQ9-3 />
#                    <PHQ9-4 />
#                    <PHQ9-5 />
#                    <PHQ9-6 />
#                    <PH9-7 />
#                    <PHQ9-8 />
#                    <PHQ9-9 />
#                    <question_9_score_is_phq9-9 />
#                    <PHQ9_TOTAL />
#                    <PHQ9_GRAND_TOTAL />
#                    <PHQ-9_SCREENING_COMPLETED_BY />
#                    <Or />
#                    <Thanking_patient_for_PHQ9 />
#                </PHQ-9>
#            </phq9>
#            <Functioning>
#                <FUNCTIONING>
#                    <FIELD_ACTIVITIES />
#                    <HOUSEHOLD_ACTIVITIES />
#                    <Work_and_school_functioning />
#                    <SOCIAL_FUNCTIONING />
#                    <PERSONAL_HYGIENE />
#                    <Functioning_Total />
#                    <FX_total />
#                    <PSYCHOEDUCATION />
#                </FUNCTIONING>
#            </Functioning>
#            <one_month_follow_up />
#            <PSYCHO_EDUCATION_COMPLETED_BY />
#            <VHT_assigned_to_patient />
#            <refferal_date />

    #######################################################################
    # One-month Followup for Soroti
    #######################################################################
    "http://openrosa.org/formdesigner/C19F6E0E-88DA-4333-A819-714490270DC3": {
        'initial_visit': '0!',
        'followup_visit': '1!',
        'preipt_visit': '0!',
        'region': 'Soroti!',
        'case_id': 'case/@case_id',
        'form_name': '@name',
        'phq9_9': 'PHQ9/PHQ9-9',
        'phq9_total': 'PHQ9/PHQ9_TOTAL',
        'functioning_total': 'Functioning/Functioning_Total',
    },

#            <PHQ9>
#                <PHQ9-1 />
#                <PHQ9-2 />
#                <PHQ9-3 />
#                <PHQ9-4 />
#                <PHQ9-5 />
#                <PHQ9-6 />
#                <PHQ9-7 />
#                <PHQ9-8 />
#                <PHQ9-9 />
#                <SCORE />
#                <PHQ9_TOTAL />
#                <PHQ9_total_2 />
#                <Or />
#                <Thanks_for_PHQ9 />
#            </PHQ9>
#            <Functioning>
#                <FIELD_ACTIVITIES />
#                <HOUSEHOLD_ACTIVITIES />
#                <WORK_SCHOOL_FUNCTIONING />
#                <SOCIAL_FUNCTIONING />
#                <PERSONAL_HYGIENE />
#                <Functioning_Total />
#                <question2 />
#                <Next_for_patient />
#            </Functioning>

    ########################################################################
    ## Pre-IPT Followup for Soroti
    ########################################################################
    "http://openrosa.org/formdesigner/ACC11BB4-5F60-41A9-8B54-D871D7E00718": {
        'region': 'Soroti!',
        'initial_visit': '0!',
        'followup_visit': '0!',
        'preipt_visit': '1!',
        'case_id': 'case/@case_id',
        'form_name': '@name',
        'phq9_9': 'PHQ9-9',
        'phq9_total': 'question4',
        'functioning_total': 'question1',
    },
#
#            <phq9 />
#            <PHQ9 />
#            <PHQ9-1 />
#            <PHQ9-2 />
#            <PHQ9-3 />
#            <PHQ9-4 />
#            <PHQ9-5 />
#            <PHQ9-6 />
#            <PHQ9-7 />
#            <PHQ9-8 />
#            <PHQ9-9 />
#            <question4 />
#            <phq9_total_is />
#            <PHQ9-10 />
#            <FUNCTIONING>
#                <FIELD_ACTIVITIES />
#                <HOUSEHOLD_ACTIVITIES />
#                <WORK_SCHOOL_FUNCTIONING />
#                <SOCIAL_FUNCTIONING />
#                <PERSONAL_HYGIENE />
#                <question1 />
#                <question2 />
#                <Thoughts_on_suicide>
#                    <SC1 />
#                    <SC2 />
#                    <notes_regarding_action_taken_to_end_life />
#                    <SC3 />
#                </Thoughts_on_suicide>
#            </FUNCTIONING>

    #######################################################################
    # Initial Screening for Kitgum
    #######################################################################
    "http://openrosa.org/formdesigner/C9C86EE2-1896-4197-9481-4E94523CBDA3": {
        'region': 'Kitgum!',
        'initial_visit': '1!',
        'followup_visit': '0!',
        'preipt_visit': '0!',
        'case_id': 'case/@case_id',
        'form_name': '@name',
        'visit_date': 'Date',
        'employment': 'employment',
        'parish': 'parish',
        'age': 'age',
        'tribe': 'Ethnicity?',
        'religion': 'religion?',
        'marital_status': 'marital_status',
        'num_children': 'children_no',
        'education_level': 'education_level',
        'sub_county': 'sub-county?',
        'district': 'District?',
        'village': 'village?',
        'live_with': 'live_with',
        'household_head': 'hh_head',
        'phq2_total': 'PHQ2/PHQ_TOTAL',
        'phq9_9': 'PHQ9/PHQ9/PHQ9_9',
        'phq9_total': 'PHQ9/PHQ9/PHQ9_GRAND_TOTAL',

        'psychoeducation_flag': 'CPA/PSY_GIVEN_TO_POATIENT_',
        'functioning_total': 'FUNCTIONING/Functioning/Fx_total'
    },
#            <Kname />
#            <KID />
#            <Date />
#            <District />
#            <describe />
#            <sub-county />
#            <village />
#            <parish />
#            <Telphone />
#            <age />
#            <Ethnicity />
#            <religion />
#            <other_religions />
#            <marital_status />
#            <children_no />
#            <education_level />
#            <employment />
#            <Describe />
#            <home />
#            <hh_head />
#            <live_with />
#            <Others_specfiy_ />
#            <PHQ2>
#                <PHQ2_1 />
#                <PHQ2_2 />
#                <PHQ_TOTAL />
#                <PHQ2_TOTAL />
#                <completed_by />
#                <Thank_to_the_patient />
#            </PHQ2>
#            <PHQ9>
#                <PHQ9>
#                    <PHQ9_1 />
#                    <PHQ9_2 />
#                    <PHQ9_3 />
#                    <PHQ9_4 />
#                    <PHQ9_5 />
#                    <PHQ9_6 />
#                    <PHQ9_7 />
#                    <PHQ9_8 />
#                    <PHQ9_9 />
#                    <question_9_score_is_phq9_9 />
#                    <PHQ9_GRAND_TOTAL />
#                    <PHQ9_TOTAL />
#                    <PHQ-9_SCREENING_COMPLETED_BY />
#                    <PHQ9_10 />
#                    <Thanking_patient_for_PHQ9 />
#                </PHQ9>
#            </PHQ9>
#            <FUNCTIONING>
#                <Functioning>
#                    <field_activities />
#                    <hh_activities />
#                    <workl />
#                    <social />
#                    <personal_hygiene />
#                    <Fx_total />
#                    <Functioning_total />
#                </Functioning>
#            </FUNCTIONING>
#            <CPA>
#                <cpa_notes />
#                <PSY_GIVEN_TO_POATIENT_ />
#                <does_patient_qualify_for_one_month_follow_up />
#                <psychoeducation_completed_by />
#                <cpa_assigned_to_patient />
#                <refferal_date />
#            </CPA>

    #######################################################################
    # Followup for Kitgum
    #######################################################################
    "http://openrosa.org/formdesigner/0F9A0958-EF12-4AC7-BCE2-CDFA094092E4": {
        'region': 'Kitgum!',
        'initial_visit': '0!',
        'followup_visit': '1!',
        'preipt_visit': '0!',
        'case_id': 'case/@case_id',
        'form_name': '@name',
        'phq9_9': 'PHQ9/PHQ9_9',
        'phq9_total': 'PHQ9/PHQ9_TOTAL',
        'functioning_total': 'fx/Functioning/Functioning_total',
    },

#            <ID />
#            <PHQ9>
#                <PHQ9_1 />
#                <PHQ9_2 />
#                <PH9_3 />
#                <PHQ9_4 />
#                <PHQ9_5 />
#                <PHQ9_6 />
#                <PHQ9_7 />
#                <PHQ9_8 />
#                <PHQ9_9 />
#                <PHQ9_TOTAL />
#                <PHQ9_TOT />
#            </PHQ9>
#            <PHQ9_10 />
#            <Thanks_for_PHQ9 />
#            <fx>
#                <Functioning>
#                    <field_activities_ />
#                    <HH_Activities />
#                    <WORK_SCHOOL />
#                    <SOCIAL />
#                    <question6 />
#                    <Functioning_total />
#                    <fx_total />
#                    <Next_for_patient />
#                </Functioning>
#            </fx>

    #######################################################################
    # Pre-IPT for Kitgum
    #######################################################################
    "http://openrosa.org/formdesigner/5DEA8734-98FB-4D72-9A41-78B8761208BE": {
        'region': 'Kitgum!',
        'initial_visit': '0!',
        'followup_visit': '0!',
        'preipt_visit': '1!',
        'case_id': 'case/@case_id',
        'form_name': '@name',
        'phq9_9': 'PHQ9/PHQ9_9',
        'phq9_total': 'PHQ9/PHQ9_TOTAL',
        'functioning_total': 'functioning/functioning/functioning_total',
    },

#            <PHQ9>
#                <PHQ9_1 />
#                <PHQ9_2 />
#                <PHQ9_3 />
#                <PHQ9_4 />
#                <PHQ9_5 />
#                <PHQ9_6 />
#                <PHQ9_7 />
#                <PHQ9_8 />
#                <PHQ9_9 />
#                <question9_total />
#                <PHQ9_TOTAL />
#                <phq9totql />
#                <PHQ9_10 />
#                <thanks_for_phq9 />
#                <functioning>
#                    <functioning>
#                        <Field_activities />
#                        <HH_activities />
#                        <work_school_functining />
#                        <socail_functioning />
#                        <personal_hygiene />
#                        <functioning_total />
#                        <functioning_tot />
#                        <sc1 />
#                        <sc2 />
#                        <do_you_plan_to_end_your_life_in_thenext_two_weeks />
#                    </functioning>
#                </functioning>
#            </PHQ9>

    #######################################################################
    # IMPACTS (ignore for now)
    #######################################################################
    "http://openrosa.org/formdesigner/645A4A39-54A6-413E-B8E6-42171FD79745": {
    },

#                <demographics>
#                <ID />
#                <name_ />
#                <date />
#                <county />
#                <subcounty />
#                <Parishes_ />
#                <village_ />
#                <next_of_keen />
#                <phone_ />
#                <LC1 />
#                <sex />
#                <age />
#                <ethnicity />
#                <religion_ />
#                <maritalstatus_ />
#                <children_ />
#                <highest_level_of_education />
#                <employment />
#                <describe />
#                <homeown />
#                <Livewith />
#                <specify />
#                <hh_head />
#                <orphan />
#            </demographics>
#            <phq2>
#                <PHQ2-1 />
#                <PHQ2-2 />
#                <PHQ2_total />
#                <phq2_total_phq2_total />
#                <phq2_total_completed_ />
#            </phq2>
#            <phq9>
#                <PHQ9>
#                    <PHQ9-1 />
#                    <PHQ9-2 />
#                    <PHQ9-3 />
#                    <PHQ9-4 />
#                    <PHQ9-5 />
#                    <PHQ9-6 />
#                    <PHQ9-7 />
#                    <PHQ9-8 />
#                    <PHQ9-9 />
#                    <PHQ9_Total />
#                    <phq9total />
#                    <PHQ9-10 />
#                </PHQ9>
#            </phq9>
#            <Suicice_assesment_>
#                <suicide1 />
#                <descrobe3 />
#                <ii-s />
#                <question9 />
#                <iii-s />
#                <kame_eba_arabo_lieniang_mi_dano_tatamo_ni_iyik_mere_buti_if_yes_or_unsure_a />
#            </Suicice_assesment_>
#            <Functioning>
#                <FX1 />
#                <FX2 />
#                <FX3 />
#                <FX4 />
#                <FX5 />
#                <FX_TOTAL />
#                <functioning_total_fx_total />
#            </Functioning>
#            <Screening_for_alcohol_>
#                <Alcohol_screening />
#                <Cage1 />
#                <Cage_2 />
#                <Cage3 />
#                <Cage4 />
#                <Mean_drinks_ />
#                <any_other_ />
#                <specify />
#                <Cage_TT />
#                <TTCAGE />
#            </Screening_for_alcohol_>
#            <Abuse_assesment>
#                <AS1 />
#                <as2 />
#                <Who />
#                <Number_of_times_ />
#                <kweti_kabedere_me_aporeso_iya_amapu_me_kom_mi_bul_anyutin_makesin_iepone_al />
#                <As3 />
#                <if_yes_who />
#                <No_of_times />
#                <as_4 />
#            </Abuse_assesment>
#            <PSYCHLOPS>
#                <a1 />
#                <b1 />
#                <a2 />
#                <b2 />
#                <b3 />
#                <b33 />
#                <a4 />
#                <Total_psy />
#                <Total_PSYCHLOPS_ />
#            </PSYCHLOPS>
}
