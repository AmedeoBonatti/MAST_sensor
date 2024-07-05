//% color="#da43ad" iconWidth=50 iconHeight=40
namespace robot{
/*    
    //% block="import libraries" blockType="command"
    export function importLibraries(parameter: any, block: any) {
        Generator.addImport(`import binascii`);
        Generator.addImport(`import serial`);
		Generator.addImport(`import time`);
        Generator.addImport(`from PetoiRobot import *`);
    }
*/

    //% block="Read sensor data for [TIME] seconds; [LABEL] label for AI" blockType="reporter"
    //% TIME.shadow="number" TIME.defl=10
    //% LABEL.shadow="string" LABEL.defl="label"
    export function read_sensors(parameter: any, block: any) {
        let read_time = parameter.TIME.code
        let label = parameter.LABEL.code
        Generator.addImport(`from sensors import *`);
		Generator.addCode(`read_sensors(${read_time}, ${label})`);
    }

    //% block="Save sensor data [DATA] locally to [PATH]" blockType="command"
    //% DATA.shadow="normal"
    //% PATH.shadow="string" PATH.defl="test"
    export function save_sensor_data(parameter: any, block: any) {
        let data = parameter.DATA.code
        let save_name = parameter.PATH.code
        
        Generator.addImport(`from sensors import *`);
        Generator.addCode(`# This block saves the sensor data to the following directories:`)
        Generator.addCode(`# Windows: C:\\Users\\{your user name}\\sensor_data`)
        Generator.addCode(`# MacOS: /Users/{your user name}/sensor_data`)
        Generator.addCode(`# Linux: /home/{your user name}/sensor_data`)
        Generator.addCode(`# Please enter the filename in the block`)
        Generator.addCode(`save_sensor_data(${data}, ${save_name})`)
    }
}
