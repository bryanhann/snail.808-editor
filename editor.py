#Reset the "B_Temp" register on start-up just to be safe.
B_Temp=""

while True:

    clear
    #This is a while true loop, the "B_Temp" register
    #may be used later in this script to hold the input of "read".
    #
    #Typing the character "-" will end the "read" session,
    #and the value will be saved to the variable "B"
    #
    #Before reading the user's input, an initial value will be printed.
    #This "initial value" is the original contents of the
    #file to be edited (the file as mention in ${1}.)
    #Or it may be the contents held in the "B_Temp" register,
    #which is stored right before exiting this script,
    #just in case the user would like to return to the editing session.
    #
    #Unlike the direct output of "echo" or "printf",
    #This "initial value" can be edited (back-spaced) by users
    #with direct input in the "read" session.
    #
    #If the "B_Temp" register is not empty,
    #take its contents to be the initial value of "read".
    if B_Temp:

        read -e -i "$B_Temp" -d - B

    #but if "B_Temp" is empty,
    #(and if the file to be edited, as mention in ${1}, exists,)
    #then just read from the file to be edited.
    elif [[ -e ${1} ]] ; then

        read -e -i "$(<${1})" -d - B

    #but if the file to be edited does not exist,
    #do not read anything,
    #just let "echo" create the file later.
    else

        read -d - B

    fi

    #Now that the input is read,
    #the user will be given three options:
    #1) To return to the session, press "+" and enter,
    #2) To exit without saving, press "-" and enter,
    #3) To exit and save, just press enter.
    #This value will be saved to the variable "C"
    read -p $'\e[0;94m    End of Session. "+" return, "-" discard, "Enter" save.\e[0m' C

    #Do option 3. (To exit and save, just press enter.)
    if [[ "$C" = "" ]] ; then

        echo -n "${B}" > ${1}
        break


    #Do option 1. (To return to the session, press "+" and enter.)
    elif [[ $C = "+" ]] ; then

        B_Temp=${B}


    #Do option 2. (To exit without saving, press "-" and enter.)
    elif [[ $C = "-" ]] ; then

        #Just to be safe, the user will be asked
        #if the edited text should be discarded.
        #
        #the user will thus be given two options:
        #1) To return to the session, press "0" and enter,
        #2) To close without saving (discard changes), just press enter.
        #
        #To be even safer, if the user types nonsense, return also to session.
        while true ; do

            #The user can only type one character,
            #and the input will be interpreted without the need of pressing enter.
            read -p $'\e[1A\e[K　　\e[0;91mDISCARD　enter 0 to return.\e[0m' -n 1 D
                :

            #Do option 2. (To close without saving (discard changes), just press enter.)
            if   [[ $D = "" ]] ; then

                exit 0

            #Do option 1. (To return to the session, press "0" and enter.)
            #To go back to the session, the input will have to be read back to "read",
            #so the input will be saved to the "B_Temp" register to be read by "read".
            elif [[ $D = "0" ]] ; then

                B_Temp=${B}
                break

            #User typed nonsense,
            #so just do option 1 as well (return to the session).
            #To go back to the session, the input will have to be read back to "read",
            #so the input will be saved to the "B_Temp" register to be read by "read".
            else

                B_Temp=${B}
                break

            fi

        done


    #But if the user typed nonsense before any exit options,
    #display the options again, and return to session.
    else

        B_Temp=${B}
        echo -e "\e[1A\e[K    \e[0;91mAt exit options, type "+" to return, "-" to discard, "Enter" to save"
        read -p $'    \e[0;91m--RETURN AND TRY AGAIN--\e[0m'
            :


    fi

done
