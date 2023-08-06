
import uuid
import base64



def gen_guid():
    return str(uuid.uuid4())


def gen_emf_uuid():
    uid = uuid.uuid4()  
    uid_bytes = uid.bytes 
    uidenc = base64.b64encode(uid_bytes, b'-_')
    uidenc = uidenc.replace(b'=', b'')  
    res = '_' + uidenc.decode('ascii')
    return res




# this is the origianl implementation by EMF
#
#private static final class UUID
#  {
#    public synchronized static String generate()
#    {
#      updateCurrentTime();

#      // Do a base 64 conversion by turning every 3 bytes into 4 base 64 characters
#      //
#      for (int i = 0; i < 5; ++i)
#      {
#        buffer[4 * i + 1] = BASE64_DIGITS[(uuid[i * 3] >> 2) & 0x3F];
#        buffer[4 * i + 2] = BASE64_DIGITS[((uuid[i * 3] << 4) & 0x30) | ((uuid[i * 3 + 1] >> 4) & 0xF)];
#        buffer[4 * i + 3] = BASE64_DIGITS[((uuid[i * 3 + 1] << 2) & 0x3C) | ((uuid[i * 3 + 2] >> 6) & 0x3)];
#        buffer[4 * i + 4] = BASE64_DIGITS[uuid[i * 3 + 2] & 0x3F];
#      }

#      // Handle the last byte at the end.
#      //
#      buffer[21] = BASE64_DIGITS[(uuid[15] >> 2) & 0x3F];
#      buffer[22] = BASE64_DIGITS[(uuid[15] << 4) & 0x30];

#      return new String(buffer);
#    }
    
#    public synchronized static void generate(byte [] uuid)
#    {
#      updateCurrentTime();
#      System.arraycopy(UUID.uuid, 0, uuid, 0, 16);
#    }

#    private UUID()
#    {
#      super();
#    }

#    private static final char[] BASE64_DIGITS = {
#      'A',
#      'B',
#      'C',
#      'D',
#      'E',
#      'F',
#      'G',
#      'H',
#      'I',
#      'J',
#      'K',
#      'L',
#      'M',
#      'N',
#      'O',
#      'P',
#      'Q',
#      'R',
#      'S',
#      'T',
#      'U',
#      'V',
#      'W',
#      'X',
#      'Y',
#      'Z',
#      'a',
#      'b',
#      'c',
#      'd',
#      'e',
#      'f',
#      'g',
#      'h',
#      'i',
#      'j',
#      'k',
#      'l',
#      'm',
#      'n',
#      'o',
#      'p',
#      'q',
#      'r',
#      's',
#      't',
#      'u',
#      'v',
#      'w',
#      'x',
#      'y',
#      'z',
#      '0',
#      '1',
#      '2',
#      '3',
#      '4',
#      '5',
#      '6',
#      '7',
#      '8',
#      '9',
#      '-',
#      '_' };

#    /**
#     * An adjustment to convert the Java epoch of Jan 1, 1970 00:00:00 to
#     * the epoch required by the IETF specification, Oct 15, 1582 00:00:00.
#     */
#    private static final long EPOCH_ADJUSTMENT = new GregorianCalendar(1970, 0, 1, 0, 0, 0).getTime().getTime()
#      - new GregorianCalendar(1582, 9, 15, 0, 0, 0).getTime().getTime();

#    private static long lastTime = System.currentTimeMillis() + EPOCH_ADJUSTMENT;

#    private static short clockSequence;

#    private static short timeAdjustment;
    
#    private static int sleepTime = 1;

#    /**
#     * A cached array of bytes representing the UUID. The second 8 bytes
#     * will be kept the same unless the clock sequence has changed.
#     */
#    private static final byte[] uuid = new byte [16];

#    private static final char[] buffer = new char [23];

#    static
#    {
#      Random random = new SecureRandom();

#      clockSequence = (short)random.nextInt(16384);
#      updateClockSequence();

#      // Generate a 48 bit node identifier; 
#      // This is an alternative to the IEEE 802 host address, which is not available in Java.
#      //
#      byte[] nodeAddress = new byte [6];

#      random.nextBytes(nodeAddress);

#      // Set the most significant bit of the first octet to 1 so as to distinguish it from IEEE node addresses
#      //
#      nodeAddress[0] |= (byte)0x80;

#      // The node identifier is already in network byte order, 
#      // so there is no need to do any byte order reversing.
#      //
#      for (int i = 0; i < 6; ++i)
#      {
#        uuid[i + 10] = nodeAddress[i];
#      }

#      buffer[0] = '_';
#    }

#    /**
#     * Updates the clock sequence portion of the UUID. The clock sequence
#     * portion may seem odd, but in the specification, the high order byte
#     * comes before the low order byte. The variant is multiplexed into the
#     * high order octet of clockseq_hi.
#     */
#    private static void updateClockSequence()
#    {
#      // clockseq_hi
#      uuid[8] = (byte)(((clockSequence >> 8) & 0x3F) | 0x80);
#      // clockseq_low
#      uuid[9] = (byte)(clockSequence & 0xFF);
#    }

#    /**
#     * Updates the UUID with the current time, compensating for the fact
#     * that the clock resolution may be less than 100 ns. The byte array
#     * will have its first eight bytes populated with the time in the
#     * correct sequence of bytes, as per the specification.
#     */
#    private static void updateCurrentTime()
#    {
#      // Get the current time in milliseconds since the epoch 
#      // and adjust it to match the epoch required by the specification.
#      //
#      long currentTime = System.currentTimeMillis() + EPOCH_ADJUSTMENT;

#      if (lastTime > currentTime)
#      {
#        // The system clock has been rewound so the clock sequence must be incremented 
#        // to ensure that a duplicate UUID is not generated.
#        //
#        ++clockSequence;

#        if (16384 == clockSequence)
#        {
#          clockSequence = 0;
#        }

#        updateClockSequence();
#      }
#      else if (lastTime == currentTime)
#      {
#        // The system time hasn't changed so add some increment of 100s of nanoseconds to guarantee uniqueness.
#        //
#        ++timeAdjustment;

#        if (timeAdjustment > 9999)
#        {
#          // Wait so that the clock can catch up and the time adjustment won't overflow.
#          try
#          {
#            Thread.sleep(sleepTime);
#          }
#          catch (InterruptedException exception)
#          {
#            // We just woke up.
#          }

#          timeAdjustment = 0;
#          currentTime = System.currentTimeMillis() + EPOCH_ADJUSTMENT;

#          while (lastTime == currentTime)
#          {
#            try
#            {
#              ++sleepTime;
#              Thread.sleep(1);
#            }
#            catch (InterruptedException exception)
#            {
#              // We just woke up.
#            }
#            currentTime = System.currentTimeMillis() + EPOCH_ADJUSTMENT;
#          }
#        }
#      }
#      else
#      {
#        timeAdjustment = 0;
#      }

#      lastTime = currentTime;

#      // Since the granularity of time in Java is only milliseconds, 
#      // add an adjustment so that the time is represented in 100s of nanoseconds.
#      // The version number (1) is multiplexed into the most significant hex digit.
#      //
#      currentTime *= 10000;
#      currentTime += timeAdjustment;
#      currentTime |= 0x1000000000000000L;

#      // Place the time into the byte array in network byte order.
#      //
#      for (int i = 0; i < 4; ++i)
#      {
#        // time_low
#        //
#        uuid[i] = (byte)((currentTime >> 8 * (3 - i)) & 0xFFL);
#      }

#      for (int i = 0; i < 2; ++i)
#      {
#        // time_mid
#        //
#        uuid[i + 4] = (byte)((currentTime >> 8 * (1 - i) + 32) & 0xFFL);
#      }

#      for (int i = 0; i < 2; ++i)
#      {
#        // time_hi
#        //
#        uuid[i + 6] = (byte)((currentTime >> 8 * (1 - i) + 48) & 0xFFL);
#      }
#    }
#  }